import json
from dotenv import load_dotenv
import os

from knowledge_graph_from_docs import json_chunks, load_json_file
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_neo4j import Neo4jVector
from langchain_neo4j import Neo4jGraph
from knowledge_graph_from_docs import json_chunks
from knowledge_graph_from_docs import neo4j_graph, neo4j_vector_store

load_dotenv()

# Create the embeddings
openai_embeddings = OpenAIEmbeddings()

# Generate embeddings for all chunks
chunk_embeddings = []
for product in json_chunks:
    for chunk in product["chunks"]:
        embedding = openai_embeddings.embed_query(chunk)
        chunk_embeddings.append({
            "product_id": product["id"],
            "chunk_text": chunk,
            "embedding": embedding
        })

# Insert product nodes
products = load_json_file("data/products.json")

for product in products:
    product_query = """
    MERGE (p:Product {id: $id, name: $name, brand: $brand, category: $category, price: $price, description: $description})
    """
    neo4j_graph.query(product_query, product)

# Insert chunk nodes and link to products
for chunk_data in chunk_embeddings:
    chunk_query = """
    MATCH (p:Product {id: $product_id})
    MERGE (c:Chunk {productID: $product_id, text: $chunk_text, embedding: $embedding})
    MERGE (p)-[:HAS_CHUNK]->(c)
    """
    neo4j_graph.query(chunk_query, chunk_data)


