from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_neo4j import Neo4jVector
from knowledge_graph_from_docs import neo4j_graph, neo4j_vector_store
from dotenv import load_dotenv
from knowledge_graph_from_docs import json_chunks
import os

load_dotenv()

# Initialize the embeddings
openai_embeddings = OpenAIEmbeddings()

# Create a new Neo4jVector from the existing Chunk nodes
vector_store = Neo4jVector(
    graph= neo4j_graph,
    embedding=openai_embeddings,
    index_name="Chunk"
)

__all__ = [vector_store]