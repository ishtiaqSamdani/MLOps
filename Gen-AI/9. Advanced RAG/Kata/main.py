import os
import json
import requests
from urllib.parse import urlparse
from typing import List, Dict, Any, Optional

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Milvus
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from dotenv import load_dotenv
from pymilvus import utility, connections

from PyPDF2 import PdfReader
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder

load_dotenv()

class DocumentLoader:
    """
    A class to load documents from various sources like web pages and PDFs.
    """
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _get_file_path(self, url):
        """Generate a local file path for a given URL."""
        try:
            url_path = urlparse(url).path
            filename = os.path.basename(url_path)
            if not filename:
                filename = "index.html"
            # Sanitize filename
            filename = "".join(c for c in filename if c.isalnum() or c in ('.', '_', '-')).rstrip()
            return os.path.join(self.data_dir, filename)
        except Exception as e:
            print(f"Error generating file path for {url}: {e}")
            return None


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

    def load_from_pdf_url(self, url):
        """Downloads and loads a PDF from a URL."""
        print(f"Fetching PDF from {url}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            file_path = self._get_file_path(url)
            if not file_path.endswith('.pdf'):
                file_path += '.pdf'

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Saved PDF to {file_path}")
            loader = PyPDFLoader(file_path)
            return loader.load()
        except requests.RequestException as e:
            print(f"Error fetching PDF from {url}: {e}")
            return None
    
    def load_from_local_pdf(self, file_path):
        """Loads a document from a local PDF file using PyPDF2."""
        print(f"Loading document from local path: {file_path}...")
        if not os.path.exists(file_path):
            print(f"Error: File not found at {file_path}")
            return None
        try:
            reader = PdfReader(file_path)
            docs: List[Document] = []
            title = "unknown"
            try:
                meta = reader.metadata or {}
                title = str(getattr(meta, "title", None) or meta.get("/Title") or "unknown")
            except Exception:
                title = "unknown"
            for idx, page in enumerate(reader.pages):
                try:
                    text = page.extract_text() or ""
                except Exception:
                    text = ""
                page_num = str(idx + 1)
                docs.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": file_path,
                            "doc_type": "pdf",
                            "title": title,
                            "published_date": "unknown",
                            "page": page_num,
                            "section": "unknown",
                            "company": "NVIDIA",
                        },
                    )
                )
            print(f"Loaded {len(docs)} page(s) from {file_path}")
            return docs
        except Exception as e:
            print(f"Error loading local PDF {file_path}: {e}")
            return None

    def load_documents(self, sources):
        """
        Loads documents from a list of sources (can be web pages, PDF URLs, or local PDF paths).
        """
        all_docs = []
        for source in sources:
            docs = None
            if source.startswith('http://') or source.startswith('https://'):
                if source.endswith('.pdf'):
                    docs = self.load_from_pdf_url(source)
                else:
                    docs = self.load_from_web(source)
                    # Enrich web docs
                    print("#################################################################33")
                    print(docs[0])
                    print("#################################################################33")
                    if docs:
                        for d in docs:
                            d.metadata = {
                                "source": d.metadata.get("source", source),
                                "doc_type": "web",
                                "title": d.metadata.get("title", "unknown"),
                                "published_date": d.metadata.get("published_date", "unknown"),
                                "page": "unknown",
                                "section": self._infer_section_from_url(source),
                                "company": "NVIDIA",
                            }
            elif os.path.exists(source):
                if source.endswith('.pdf'):
                    docs = self.load_from_local_pdf(source)
                else:
                    print(f"Unsupported local file type for: {source}")
            else:
                print(f"Warning: Source not found or not a valid URL: {source}")
            
            if docs:
                all_docs.extend(docs)
        return all_docs

    def _infer_section_from_url(self, url: str) -> str:
        try:
            path = urlparse(url).path.strip("/")
            if not path:
                return "root"
            return path.split("/")[0]
        except Exception:
            return "unknown"


class VectorDB:
    """
    A class to handle vector database operations with Milvus.
    """
    def __init__(self, host="localhost", port="19530"):
        self.host = host
        self.port = port
        # Use Hugging Face embeddings: nomic-ai/nomic-embed-text-v1.5
        print("Initializing Hugging Face embeddings 'nomic-ai/nomic-embed-text-v1.5'...")
        self.embedding_function = HuggingFaceEmbeddings(
            model_name="nomic-ai/nomic-embed-text-v1.5",
            model_kwargs={"trust_remote_code": True},
        )

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
                return Milvus(
                    embedding_function=self.embedding_function,
                    connection_args={"host": self.host, "port": self.port},
                    collection_name=collection_name,
                )
        print("Processing and storing documents in Milvus...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )
        docs = text_splitter.split_documents(documents)

        print("#######################################################################")
        print(f"Split {len(documents)} documents into {len(docs)} chunks.")
        print("#######################################################################")

        # Ensure uniform metadata schema across ALL chunks (all values as strings)
        uniform_keys = ["source", "doc_type", "title", "published_date", "page", "section", "company"]
        for d in docs:
            md = d.metadata or {}
            normalized: Dict[str, str] = {}
            for k in uniform_keys:
                v = md.get(k, "unknown")
                normalized[k] = str(v)
            d.metadata = normalized

        # Prefix content with task instruction for nomic model
        for d in docs:
            d.page_content = f"search_document: {d.page_content or ''}"

        vector_db = Milvus.from_documents(
            docs,
            self.embedding_function,
            connection_args={"host": self.host, "port": self.port},
            collection_name=collection_name
        )
        print(f"Successfully stored {len(docs)} document chunks in collection '{collection_name}'.")
        return vector_db


class QueryConstructor:
    """
    Constructs a retrieval-oriented query and optional filters using an LLM.
    Returns a dict: { search_query: str, filters: { doc_type?: str, must_include?: [str], sections?: [str], date_range?: {from,to} } }
    """
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.1)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Rewrite the user's question into a short search query and decide optional filters in strict JSON.\n"
                           "Output ONLY JSON with keys: search_query (string), filters (object with optional keys: doc_type (string), must_include (array of strings), sections (array of strings))."),
                ("human", "{question}")
            ]
        )

    def construct(self, question: str) -> Dict[str, Any]:
        try:
            text = (self.prompt | self.llm | StrOutputParser()).invoke({"question": question})
            data = json.loads(text)
            if not isinstance(data, dict) or "search_query" not in data:
                raise ValueError("Invalid JSON structure")
            if "filters" not in data or not isinstance(data["filters"], dict):
                data["filters"] = {}
            return data
        except Exception:
            # Fallback
            return {"search_query": question, "filters": {}}


class Reranker:
    """
    Cross-encoder reranker using sentence-transformers.
    """
    def __init__(self, model_name: str = "BAAI/bge-reranker-base"):
        print(f"Loading cross-encoder reranker: {model_name} ...")
        self.model = CrossEncoder(model_name, max_length=512)

    def rerank(self, query: str, docs: List[Document], top_k: int = 6) -> List[Document]:
        if not docs:
            return []
        pairs = [(query, d.page_content) for d in docs]
        scores = self.model.predict(pairs)
        scored = list(zip(docs, scores))
        scored.sort(key=lambda x: float(x[1]), reverse=True)
        return [d for d, _ in scored[:top_k]]


class RAGSystem:
    """
    The main RAG system class.
    """
    def __init__(self, vector_db):
        self.vector_db = vector_db
        self.llm = ChatOpenAI(temperature=0.1)
        self.query_constructor = QueryConstructor()
        self.reranker = Reranker()

    def query(self, question):
        print(f"\nPerforming Advanced RAG query: '{question}'")
        qc = self.query_constructor.construct(question)
        search_query: str = qc.get("search_query", question)
        filters: Dict[str, Any] = qc.get("filters", {})
        doc_type_filter: Optional[str] = filters.get("doc_type")
        must_include: List[str] = filters.get("must_include", [])
        sections_filter: List[str] = filters.get("sections", [])

        print(f"- Constructed search query: {search_query}")
        if doc_type_filter:
            print(f"- Filter doc_type: {doc_type_filter}")
        if sections_filter:
            print(f"- Filter sections: {sections_filter}")
        if must_include:
            print(f"- Terms must include: {must_include}")

        # Retrieve a broad set (prefix query for nomic model)
        try:
            retrieved: List[Document] = self.vector_db.similarity_search(f"search_query: {search_query}", k=20)
        except Exception:
            # Fallback to retriever
            retrieved = self.vector_db.as_retriever(search_kwargs={"k": 20}).invoke(f"search_query: {search_query}")

        # Client-side filter by metadata
        filtered = []
        for d in retrieved:
            md = d.metadata or {}
            if doc_type_filter and md.get("doc_type") != doc_type_filter:
                continue
            if sections_filter and md.get("section") not in sections_filter:
                continue
            if must_include and not all(term.lower() in (d.page_content or "").lower() for term in must_include):
                continue
            filtered.append(d)

        print(f"- Retrieved: {len(retrieved)} | After filter: {len(filtered)}")

        # Rerank
        top_docs = self.reranker.rerank(search_query, filtered or retrieved, top_k=6)
        print(f"- After rerank: {len(top_docs)} kept")

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

        # Build runnable combine only (retrieval handled above for reranking)
        combine = prompt | self.llm | StrOutputParser()
        context_text = "\n\n".join(d.page_content for d in top_docs)
        result_text = combine.invoke({"context": context_text, "input": question})
        result = {"answer": result_text, "context": top_docs}

        print("\n--- Query Result ---")
        print(f"Answer: {result['answer']}")
        print("Sources:")
        for doc in result["context"]:
            md = doc.metadata or {}
            print(f"- {md.get('source', 'Unknown')} "
                  f"(doc_type={md.get('doc_type','?')}, section={md.get('section','?')}, page={md.get('page','?')})")
        
        return result

def main():
    
    # --- 1. Document Loading ---
    # Using NVIDIA as an example company
    document_sources = [
        "https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-first-quarter-fiscal-2026",
        "https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2026",
        "https://investor.nvidia.com/news/press-release-details/2023/NVIDIA-Announces-Financial-Results-for-First-Quarter-Fiscal-2024/default.aspx",
        "https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2024",
        "https://investor.nvidia.com/news/press-release-details/2024/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2024/",
        "https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2025",
        "data/NVIDIA-2025-Q4.pdf",
        "data/NVIDIA-2025-Q3.pdf",
        "data/NVIDIA-2024-Q3.pdf",
    ]
    
    doc_loader = DocumentLoader()
    documents = doc_loader.load_documents(document_sources)
    print("#######################################################################")
    print(f"Loaded {len(documents)} documents")
    print("#######################################################################")

    if not documents:
        print("No documents loaded. Exiting.")
        return

    # --- 2. Vector DB Storage ---
    vector_db_manager = VectorDB()
    vector_db = vector_db_manager.store(documents)

    # --- 3. RAG System Querying ---
    rag_system = RAGSystem(vector_db)
    
    # Example queries
    # rag_system.query("What was NVIDIA's revenue in the fourth quarter of 2025? Only from pdf.")
    # rag_system.query("What was NVIDIA's revenue in the fourth quarter of 2025?")
    # rag_system.query("What was NVIDIA's revenue in the first quarter of 2026?")
    # rag_system.query("Was there a revenue drop from Q1 to Q2 of fiscal 2026? Include figures.")
    rag_system.query("Summarize Q1 FY26 data center revenue and growth vs prior quarter.")
    rag_system.query("Summarize Q1 FY25 data center revenue and growth vs prior quarter.")
    rag_system.query("Summarize Q1 FY22 data center revenue and growth vs prior quarter.")

    rag_system.query("who won cricket world cup 2025")


if __name__ == "__main__":
    print("Starting the RAG-powered Business Analysis System...")
    main()
