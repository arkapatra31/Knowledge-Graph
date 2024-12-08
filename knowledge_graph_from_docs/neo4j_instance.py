from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_neo4j import Neo4jVector
from langchain_neo4j import Neo4jGraph
from dotenv import load_dotenv
import os

load_dotenv()

# Fetch the ENV variables
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE')

# Create the embeddings
openai_embeddings = OpenAIEmbeddings()

# Create Neo4j Vector Store
neo4j_vector_store = Neo4jVector(
    embedding=openai_embeddings,
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    database=NEO4J_DATABASE
)


# Create Neo4j Graph
neo4j_graph = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    database=NEO4J_DATABASE
)

__all__ = [neo4j_vector_store, neo4j_graph]