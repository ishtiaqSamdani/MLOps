## RAG-powered Business Analysis System (Kata)

A small Retrieval-Augmented Generation pipeline that:
- Scrapes company web pages and loads local PDFs
- Chunks and embeds text using `all-MiniLM-L6-v2`
- Stores vectors in Milvus (standalone via Docker Compose)
- Answers analyst questions with sources using OpenAI Chat (LangChain Runnables)

Directory: `MLOps/Gen-AI/8. Retrieval Augmented Generation/Kata/`


### Prerequisites
- Docker and Docker Compose plugin
- Anaconda (or Miniconda)
- OpenAI API key


### 1) Start Milvus (standalone)

From this directory:

```bash
docker compose up -d
docker compose ps
# optional health check
curl -f http://localhost:9091/healthz
```

Data persists under `milvus-volumes/` in this folder (created automatically).


### 2) Configure environment

Create a `.env` file here:

```bash
cat > .env << 'EOF'
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
# Optional: customize the User-Agent used by WebBaseLoader
USER_AGENT=RAG-Analyst/1.0 (+https://example.com)
EOF
```

Or set variables in your shell:
```bash
export OPENAI_API_KEY=YOUR_OPENAI_API_KEY
export USER_AGENT="RAG-Analyst/1.0 (+https://example.com)"
```


### 3) Python environment and dependencies

Use conda base (as used in this kata):

```bash
source ~/anaconda3/etc/profile.d/conda.sh
conda activate base
pip install -r requirements.txt
```

Note: If you prefer an isolated env:
```bash
conda create -y -n rag-kata python=3.10
conda activate rag-kata
pip install -r requirements.txt
```


### 4) Documents

- Local PDFs go into `data/` (already included: `data/NVIDIA-2025-Q4.pdf`).
- Web pages are scraped directly (not saved to disk).

To change sources, edit the list in `main.py` (function `main()`).


### 5) First run (build collection and test)

Force a clean (re)index on first run:
```bash
export RAG_REINDEX=true
python main.py
```

You should see:
- Scrape logs
- “Successfully stored … chunks in collection 'business_analysis'.”
- A few demo Q&A answers with “Sources:” printed


### 6) Subsequent runs (skip re-index)

If nothing changed, just:
```bash
unset RAG_REINDEX   # or ensure it's not set to "true"
python main.py
```

To rebuild the collection at any time:
```bash
export RAG_REINDEX=true
python main.py
```


### 7) Stop or reset Milvus

Stop:
```bash
docker compose down
```

Full reset (containers, images, volumes):
```bash
docker compose down --volumes --rmi all
rm -rf milvus-volumes
```


### 8) Troubleshooting

- Milvus “ParamError: Field data size misaligned … description”  
  Use a clean rebuild:
  ```bash
  export RAG_REINDEX=true
  python main.py
  ```

- Milvus not ready / connection issues  
  Wait for health to turn ready:
  ```bash
  docker compose ps
  curl -f http://localhost:9091/healthz
  ```

- LangChain deprecation warning for `HuggingFaceEmbeddings`  
  Safe to ignore for the kata. Optionally:
  ```bash
  pip install -U langchain-huggingface
  # and switch to: from langchain_huggingface import HuggingFaceEmbeddings
  ```

- “python: command not found”  
  Make sure conda base is active:
  ```bash
  source ~/anaconda3/etc/profile.d/conda.sh
  conda activate base
  python --version
  ```


### 9) What this run prints
- Number of loaded documents and chunks
- Confirmation of vector insert into Milvus
- Short answers to sample questions
- A “Sources:” section listing the origin of retrieved chunks


### 10) Notes
- OpenAI usage may incur costs.
- Web scraping honors a configurable `USER_AGENT`.
- This kata demonstrates idempotent indexing and modern LangChain Runnable pipelines.

#### Screenshots

<img width="1900" height="1859" alt="image" src="https://github.com/user-attachments/assets/38e9cffb-5650-40fa-bb32-957c715b209a" />
<img width="1860" height="635" alt="image" src="https://github.com/user-attachments/assets/868760a7-1945-4725-b0ba-ae0540c5335b" />



