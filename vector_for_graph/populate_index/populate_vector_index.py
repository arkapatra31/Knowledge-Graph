from vector_for_graph import kg, OPENAI_API_KEY
from langchain_openai.embeddings import OpenAIEmbeddings

# Populate the vector index
# Calculate vector representation for each movie tagline using OpenAI
# Add vector to the Movie node as taglineEmbedding property

openai_embeddings = OpenAIEmbeddings()

# Query all the movies with taglines
cypher = """
  MATCH (m:Movie) 
  WHERE m.tagline IS NOT NULL 
  RETURN m.title, m.tagline
  """
movies = kg.query(cypher)

# Extract the taglines
taglines = [movie['m.tagline'] for movie in movies]

# Generate embeddings for each tagline
tagline_vectors = [openai_embeddings.embed_query(tagline) for tagline in taglines]

for tagline, vector in zip(taglines, tagline_vectors):
    # Convert the vector to a format Neo4j accepts (e.g., as a JSON array)
    vector_str = ",".join(map(str, vector))
    update_query = f"""
    MATCH (m:Movie {{tagline: $tagline}})
    SET m.tagline_embedding = [{vector_str}]
    """
    kg.query(update_query, {"tagline": tagline})


