from  vector_for_graph import kg

query = """
    MATCH (m:Movie)
    WHERE m.tagline IS NOT NULL 
    RETURN m.tagline, m.tagline_embedding
    """

results = kg.query(query)

print(len(results[0]['m.tagline_embedding']))