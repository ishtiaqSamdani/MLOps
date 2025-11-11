import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
import re

# --- 1. Load Data ---
try:
    df = pd.read_csv('data/movies-dataset.csv')
    df = df.dropna(subset=['Description', 'Genre', 'Director'])
except FileNotFoundError:
    print("Error: movies-dataset.csv not found. Make sure the path is correct.")
    exit()

# --- 2. Initialize ChromaDB and Embedding Model ---
chroma_client = chromadb.HttpClient(host='localhost', port=8000)
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collection_name = "movies"
# Delete collection if it exists
try:
    if chroma_client.get_collection(name=collection_name):
        chroma_client.delete_collection(name=collection_name)
except Exception:
    pass


collection = chroma_client.get_or_create_collection(
    name=collection_name,
    embedding_function=sentence_transformer_ef,
    metadata={"hnsw:space": "cosine"} 
)


# --- 3. Prepare and Insert Data into ChromaDB ---
documents = df['Description'].tolist()
metadatas = []
for index, row in df.iterrows():
    metadatas.append({
        'title': row['Title'],
        'genre': row['Genre'],
        'director': row['Director']
    })
ids = [f"id_{i}" for i in range(len(documents))]

# Add data to the collection in batches
batch_size = 10
for i in range(0, len(documents), batch_size):
    collection.add(
        documents=documents[i:i+batch_size],
        metadatas=metadatas[i:i+batch_size],
        ids=ids[i:i+batch_size]
    )

print(f"Added {len(documents)} movies to the '{collection_name}' collection.")

def get_recommendations(query):
    unique_genres = df['Genre'].unique()
    unique_directors = df['Director'].unique()

    filters = []
    
    # Check for genres in the query
    for genre in unique_genres:
        if re.search(r'\b' + re.escape(genre) + r'\b', query, re.IGNORECASE):
            filters.append({'genre': genre})

    # Check for directors in the query
    for director in unique_directors:
        if re.search(r'\b' + re.escape(director) + r'\b', query, re.IGNORECASE):
            filters.append({'director': director})
    where_clause = {}
    if len(filters) > 1:
        where_clause = {"$and": filters}
    elif len(filters) == 1:
        where_clause = filters[0]

    print(f"\nSearching for: '{query}'")
    print(filters)
    print(where_clause)
    if where_clause:
        print(f"Applying filters: {where_clause}")

    results = collection.query(
        query_texts=[query],
        n_results=5,
        where=where_clause if where_clause else None
    )

    # Print results
    if not results['documents'][0]:
        print("No results found.")
        return

    print("\nTop 5 Movie Recommendations:")
    for i in range(len(results['documents'][0])):
        meta = results['metadatas'][0][i]
        print(f"  - Title: {meta['title']}")
        print(f"    Genre: {meta['genre']}")
        print(f"    Director: {meta['director']}")
        print(f"    Similarity Score: {results['distances'][0][i]:.4f}")
        # print(f"    Description: {results['documents'][0][i]}") # Uncomment for full description
    print("-" * 20)


# --- Example Queries ---
get_recommendations("A space movie")
get_recommendations("A mind-bending science fiction movie by Christopher Nolan")
get_recommendations("A crime movie")
get_recommendations("A funny movie about a slacker")
