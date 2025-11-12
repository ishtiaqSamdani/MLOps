## Problems and Solutions (Kata)

This document records the issues encountered while building and running the RAG-powered Business Analysis System and how each was fixed. It includes error logs, root causes, and the exact code/commands changed.


### 1) Milvus Docker image tag not found (manifest unknown)

Error (when pulling a wrong image tag):

```bash
Error response from daemon: manifest for milvusdb/milvus:v2.4.4-standalone not found: manifest unknown: manifest unknown
```

Root cause:
- Using a non-existent Milvus image tag for a standalone deployment.

Solution:
- Switched to the official Milvus v2.6.5 standalone Docker Compose with dependent services (`etcd`, `minio`) and persistent volumes.

Key compose (excerpt):

```39:52:MLOps/Gen-AI/8. Retrieval Augmented Generation/Kata/docker-compose.yml
  standalone:
    container_name: milvus-standalone
    image: milvusdb/milvus:v2.6.5
    command: ["milvus", "run", "standalone"]
    security_opt:
    - seccomp:unconfined
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
      MQ_TYPE: woodpecker
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/milvus-volumes/milvus:/var/lib/milvus
```

Run:
```bash
docker compose up -d
docker compose ps
curl -f http://localhost:9091/healthz
```


### 2) Permission denied clearing volumes

Error (trying to delete bind-mount data created by containers as root):

```bash
rm: cannot remove 'milvus-volumes/minio/.../xl.meta': Permission denied
```

Root cause:
- Files under `milvus-volumes/` created by containers with root ownership.

Solution:
- Use a temporary container with the volume mounted to remove files as root, then remove the host directory.

Command:
```bash
docker run --rm -v "$PWD/milvus-volumes":/target alpine sh -c "find /target -mindepth 1 -maxdepth 1 -exec rm -rf {} +"
rm -rf milvus-volumes
docker compose pull && docker compose up -d
```


### 3) LangChain import breakages after upstream changes

Symptoms:

```bash
ModuleNotFoundError: No module named 'langchain.text_splitter'
```
```bash
ModuleNotFoundError: No module named 'langchain.chains'
```

Root cause:
- LangChain split some packages and deprecated older APIs (chains, text_splitter path).

Fixes:
- Use `langchain_text_splitters` for splitters
- Use Runnable-based RAG instead of deprecated `RetrievalQA` chains
- Ensure required LangChain packages are installed

Updated imports (main.py):

```1:13:MLOps/Gen-AI/8. Retrieval Augmented Generation/Kata/main.py
import os
import requests
from urllib.parse import urlparse
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Milvus
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from dotenv import load_dotenv
from pymilvus import utility, connections
```

Requirements snapshot:

```1:15:MLOps/Gen-AI/8. Retrieval Augmented Generation/Kata/requirements.txt
pymilvus
sentence-transformers
openai
langchain
langchain-core
langchain-community
langchain-openai
langchain-milvus
pypdf
beautifulsoup4
requests
python-dotenv
tiktoken
langchain-text-splitters
```

Runnable-based RAG (replacing deprecated Chains):

```186:213:MLOps/Gen-AI/8. Retrieval Augmented Generation/Kata/main.py
    def query(self, question):
        print(f"\nPerforming RAG query: '{question}'")
        retriever = self.vector_db.as_retriever()

        system_prompt = (
            "Use the given context to answer the question. "
            "If you don't know the answer, say you don't know. "
            "Use three sentences maximum and keep the answer concise. "
            "Context: {context}"
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        # Build runnable retrieval + QA
        combine = prompt | self.llm | StrOutputParser()
        answer_chain = (
            RunnableParallel(context=retriever, input=RunnablePassthrough())
            .assign(context=lambda x: "\n\n".join(d.page_content for d in x["context"]))
            | combine
        )
        rag = RunnableParallel(answer=answer_chain, context=retriever)

        result = rag.invoke(question)
```


### 4) Milvus ParamError: Field data size misaligned

Error:

```bash
RPC error: [batch_insert], <ParamError: (code=1, message=('Field data size misaligned for field [description] ', 'got size=[97] ', 'alignment size=[130]'))>
```

Root cause:
- Metadata keys were inconsistent across chunks (some had `description`, others not), causing column misalignment in Milvus.
- On subsequent runs, the old collection schema (with extra fields) mismatched new inserts.

Solutions:
1) Sanitize chunk metadata to a single, uniform key: `source` only.
2) Add idempotent indexing with `RAG_REINDEX` to drop/rebuild the collection when needed.

Code changes (metadata sanitization):

```163:167:MLOps/Gen-AI/8. Retrieval Augmented Generation/Kata/main.py
        # Sanitize metadata to avoid Milvus field size misalignment: keep only a uniform 'source' key
        for d in docs:
            src = (d.metadata or {}).get("source", "unknown")
            d.metadata = {"source": str(src)}
```

Collection reuse/reindex handling:

```130:151:MLOps/Gen-AI/8. Retrieval Augmented Generation/Kata/main.py
    def store(self, documents, collection_name="business_analysis"):
        # Ensure a Milvus connection for utility operations
        try:
            if not connections.has_connection("default"):
                connections.connect(alias="default", host=self.host, port=self.port)
        except Exception:
            connections.connect(alias="default", host=self.host, port=self.port)

        # Handle existing collection to avoid schema mismatches on reruns
        reindex = os.getenv("RAG_REINDEX", "false").lower() in ("1", "true", "yes", "y")
        if utility.has_collection(collection_name):
            if reindex:
                print(f"Dropping existing collection '{collection_name}' (RAG_REINDEX=true)...")
                utility.drop_collection(collection_name)
            else:
                print(f"Collection '{collection_name}' exists; reusing without reindex.")
                return Milvus.from_existing_collection(
                    self.embedding_function,
                    connection_args={"host": self.host, "port": self.port},
                    collection_name=collection_name,
                )
```

Run with forced rebuild:
```bash
export RAG_REINDEX=true
python main.py
```


### 5) DataNotMatchException (schema mismatch: expect 6 list, got 3)

Error:

```bash
pymilvus.exceptions.DataNotMatchException: <DataNotMatchException: (code=1, message=The data doesn't match with schema fields, expect 6 list, got 3)>
```

Root cause:
- Attempting to insert into an existing collection created earlier with a different field layout.

Solution:
- Drop the collection when `RAG_REINDEX=true` before inserting (see code above). This ensures a clean schema build.


### 6) ConnectionNotExistException (pymilvus)

Error:

```bash
pymilvus.exceptions.ConnectionNotExistException: <ConnectionNotExistException: (code=1, message=should create connection first.)>
```

Root cause:
- `pymilvus.utility.has_collection` requires an active connection.

Solution:
- Connect prior to using utility helpers (see `connections.connect(...)` in the `store` method above).


### 7) Web pages scraping without saving HTML

Requirement:
- Scrape web pages directly, do not write HTML to disk; use `data/` only for non-web PDFs.

Implementation (uses `WebBaseLoader` with a configurable `USER_AGENT`):

```41:56:MLOps/Gen-AI/8. Retrieval Augmented Generation/Kata/main.py
    def load_from_web(self, url):
        """Scrapes a web page directly into Documents without saving HTML."""
        print(f"Scraping document from {url}...")
        try:
            user_agent = os.getenv("USER_AGENT", "RAG-Analyst/1.0 (+https://example.com)")
            loader = WebBaseLoader(
                [url],
                requests_kwargs={
                    "headers": {
                        "User-Agent": user_agent
                    }
                }
            )
            docs = loader.load()
            print(f"Scraped {len(docs)} document(s) from {url}")
            return docs
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
```


### 8) Python not found vs conda base

Error:

```bash
Command 'python' not found, did you mean: python3 ...
```

Solution:
- Activate conda base and use `python` from that environment.

Commands:
```bash
source ~/anaconda3/etc/profile.d/conda.sh
conda activate base
python main.py
```


### 9) Deprecation warning for `HuggingFaceEmbeddings`

Warning:

```bash
LangChainDeprecationWarning: The class `HuggingFaceEmbeddings` was deprecated...
```

Current usage (works for this kata):

```125:129:MLOps/Gen-AI/8. Retrieval Augmented Generation/Kata/main.py
    def __init__(self, host="localhost", port="19530"):
        self.host = host
        self.port = port
        self.embedding_function = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
```

Optional (future) switch:
```bash
pip install -U langchain-huggingface
# then import from langchain_huggingface import HuggingFaceEmbeddings
```


### 10) Idempotent indexing and queries

- Document list (web + local PDF) lives in `main.py`:

```226:230:MLOps/Gen-AI/8. Retrieval Augmented Generation/Kata/main.py
    document_sources = [
        "https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-first-quarter-fiscal-2026",
        "https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2026",
        "data/NVIDIA-2025-Q4.pdf"
    ]
```

- On first run, it’s recommended to set `RAG_REINDEX=true` to create a clean collection.
- Subsequent runs can reuse the existing collection to avoid re-embedding.


### 11) Quick reference: Clean redeploy and run

```bash
# stop & remove everything (containers, images, volumes)
docker compose down --volumes --rmi all
docker run --rm -v "$PWD/milvus-volumes":/target alpine sh -c "find /target -mindepth 1 -maxdepth 1 -exec rm -rf {} +"
rm -rf milvus-volumes

# start fresh
docker compose pull && docker compose up -d

# run app
source ~/anaconda3/etc/profile.d/conda.sh
conda activate base
pip install -r requirements.txt
export OPENAI_API_KEY=YOUR_OPENAI_API_KEY
export RAG_REINDEX=true
python main.py
```

All major issues have been addressed with stable fixes that should keep the pipeline reproducible and resilient across reruns. 


