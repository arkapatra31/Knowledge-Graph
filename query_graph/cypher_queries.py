from dotenv import load_dotenv
import os
from langchain_community.graphs import Neo4jGraph

# Import warning controls
import warnings

warnings.filterwarnings("ignore")

load_dotenv()
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE')

# Initialise a Knowledge Graph
kg = Neo4jGraph(
    url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD, database=NEO4J_DATABASE
)

# Query to get all the nodes and relationships in the graph
query1 = """
MATCH (n)
RETURN n
"""
print(f"Query 2 \n Response \n ________________________\n{kg.query(query1)}")

# Query to match all the nodes with a specific label
query2 = """
MATCH (n:Person)
RETURN n
"""
print(f"Query 2 \n Response \n ________________________\n{kg.query(query2)}")


# Query to match 2 nodes with a specific label and a relationship between them
query3 = """
MATCH (p:Person)-[r:FRIEND]->(p2:Person)
RETURN p, r, p2
"""
print(f"Query 3 \n Response \n ________________________\n{kg.query(query3)}")

# Query to find which person works in which company
query4 = """
MATCH (p:Person)-[r:WORKS_IN]->(c:Company)
RETURN p, r, c
"""
print(f"Query 4 \n Response \n ________________________\n{kg.query(query4)}")

# Query to update the second person's name
query5 = """
MATCH (p:Person {name: 'PATRA'}) SET p.name = 'Jane Doe'
RETURN p
"""
print(f"Query 5 \n Response \n ________________________\n{kg.query(query5)}")


# Query to find a person who works in Deloitte and is friend with Jane Doe
query6 = """
MATCH (c:Company {company: "Deloitte"})<-[:WORKS_IN]-(p:Person)-[:FRIEND]->(p1:Person {name: "Jane Doe"})
RETURN p
"""

# Query to add a new person to the graph
query7 = """
CREATE (p:Person {name: 'John Wick', age: 30})
RETURN p
"""
print(f"Query 7 \n Response \n ________________________\n{kg.query(query7)}")

# Query to add new properties to the person node
query8 = """
MATCH (p:Person {name: 'John Wick'})
SET p.email = 'john.wick@test.com'
RETURN p
"""

# Query to delete every node and relationship in the graph
query9 = """
MATCH (n)
DETACH DELETE n
"""
print(f"Query 9 \n Response \n ________________________\n{kg.query(query9)}")



