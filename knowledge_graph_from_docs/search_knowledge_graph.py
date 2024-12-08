from langchain_openai.embeddings import OpenAIEmbeddings
from knowledge_graph_from_docs import neo4j_graph

openai_embeddings = OpenAIEmbeddings()
# Embed the user's query
query_text = "Find a gaming laptop"
query_embedding = openai_embeddings.embed_query(query_text)

# Query Neo4j for similar chunks
similarity_query = """
WITH $query_embedding AS query_embedding
MATCH (c:Chunk)<-[:HAS_CHUNK]-(p:Product)
WITH c,p, gds.similarity.cosine(query_embedding, c.embedding) AS similarity
WHERE similarity > 0.8
RETURN c.text AS chunk_text, p.id AS productId, similarity
ORDER BY similarity DESC
LIMIT 10
"""
result = neo4j_graph.query(similarity_query, {"query_embedding": query_embedding})

# Display results
relevant_chunks = [{"text": record["chunk_text"], "productId": record["productId"], "similarity": record["similarity"]} for record in result]
print("Relevant Chunks:", relevant_chunks)
