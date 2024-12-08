from tabnanny import verbose

from dotenv import load_dotenv
from knowledge_graph_from_docs import vector_store, neo4j_graph
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_neo4j.chains.graph_qa.cypher import GraphCypherQAChain

load_dotenv()

openai_embeddings = OpenAIEmbeddings()

query_text = "Suggest the best laptop for programming."


# Perform a similarity search using the query embedding on the neo4j vector store
def similarity_search():
    query_embedding = openai_embeddings.embed_query(query_text)
    docs = vector_store.similarity_search(query=query_text, k=1)
    # Print the results
    for doc in docs:
        print("Relevant Chunk:", doc.page_content)

def vector_retriever():
    # Create Vector Store retriever
    retriever = vector_store.as_retriever()
    response = retriever.invoke(query_text)
    print(response[0].page_content)


def create_chain():
    # Create a Cypher QA chain
    llm = ChatOpenAI(model_name="gpt-4o-mini", verbose=True, temperature=0.4)
    chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=neo4j_graph,
        validate_cypher=True,
        verbose=True,
        #use_function_response=True,
        allow_dangerous_requests=True
    )
    response = chain.invoke({"query": query_text})
    print(response)

if __name__ == "__main__":
    similarity_search()
    #vector_retriever()
    #create_chain()
