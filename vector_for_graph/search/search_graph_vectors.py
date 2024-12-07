from vector_for_graph import kg
from langchain_openai.embeddings import OpenAIEmbeddings

openai_embeddings = OpenAIEmbeddings()

# Question
question = "Thriller Movies?"

# Embed the question
question_embedding = openai_embeddings.embed_query(question)

query = """
WITH $question_embedding AS query_embedding
MATCH (m:Movie)
WHERE m.tagline_embedding IS NOT NULL
WITH m, gds.similarity.cosine(query_embedding, m.tagline_embedding) AS similarity
WHERE similarity > 0.7
RETURN m.title AS title, similarity
ORDER BY similarity DESC
LIMIT 10
"""

# Execute the query
result = kg.query(query, {"question_embedding": question_embedding})

# Parse and print results
movies = [{"title": record["title"], "similarity": record["similarity"]} for record in result]
print("Relevant Movies:", movies)
