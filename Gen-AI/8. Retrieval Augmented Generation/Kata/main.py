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
        """Loads a document from a local PDF file."""
        print(f"Loading document from local path: {file_path}...")
        if not os.path.exists(file_path):
            print(f"Error: File not found at {file_path}")
            return None
        try:
            loader = PyPDFLoader(file_path)
            return loader.load()
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


class VectorDB:
    """
    A class to handle vector database operations with Milvus.
    """
    def __init__(self, host="localhost", port="19530"):
        self.host = host
        self.port = port
        self.embedding_function = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

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
        print("Processing and storing documents in Milvus...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100,
        length_function=len,
        separators=["\n\n", "\n"," ",""]
        )
        docs = text_splitter.split_documents(documents)

        print("#######################################################################")
        print(f"Split {len(documents)} documents into {len(docs)} chunks.")
        print(f"Docs: {docs}")
        print("#######################################################################")

        # Sanitize metadata to avoid Milvus field size misalignment: keep only a uniform 'source' key
        for d in docs:
            src = (d.metadata or {}).get("source", "unknown")
            d.metadata = {"source": str(src)}

        vector_db = Milvus.from_documents(
            docs,
            self.embedding_function,
            connection_args={"host": self.host, "port": self.port},
            collection_name=collection_name
        )
        print(f"Successfully stored {len(docs)} document chunks in collection '{collection_name}'.")
        return vector_db


class RAGSystem:
    """
    The main RAG system class.
    """
    def __init__(self, vector_db):
        self.vector_db = vector_db
        self.llm = ChatOpenAI(temperature=0.1)

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

        print("\n--- Query Result ---")
        print(f"Answer: {result['answer']}")
        print("Sources:")
        for doc in result["context"]:
            print(f"- {doc.metadata.get('source', 'Unknown')}")
        
        return result

def main():
    
    # --- 1. Document Loading ---
    # Using NVIDIA as an example company
    document_sources = [
        "https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-first-quarter-fiscal-2026",
        "https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2026",
        "data/NVIDIA-2025-Q4.pdf"
    ]
    
    doc_loader = DocumentLoader()
    documents = doc_loader.load_documents(document_sources)
    print("#######################################################################")
    print(f"Loaded {len(documents)} documents")
    print(f"Documents: {documents}")
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
    rag_system.query("What was NVIDIA's revenue in the fourth quarter of 2025?")
    rag_system.query("What was NVIDIA's revenue in the first quarter of 2026?")
    rag_system.query("was there a  revenue frop from q1 to q2 of 2026")
    rag_system.query("Who won cricket world cup 2025")


if __name__ == "__main__":
    print("Starting the RAG-powered Business Analysis System...")
    main()
