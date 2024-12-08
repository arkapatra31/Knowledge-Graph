from tabnanny import verbose
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from knowledge_graph_from_docs import vector_store, neo4j_graph
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_neo4j.chains.graph_qa.cypher import GraphCypherQAChain
import warnings

load_dotenv()

warnings.filterwarnings("ignore")

openai_embeddings = OpenAIEmbeddings()

query_text = "Suggest a good Camera under $4000"


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


def qa_chain():
    # Create a Cypher QA chain
    llm = ChatOpenAI(model_name="gpt-4o-mini", verbose=True, temperature=0.4)

    CYPHER_GENERATION_TEMPLATE = """
    You are an expert Neo4j Developer translating user questions into Cypher to answer questions about products and related details.
    Convert the user's question based on the schema.
    Carefully consider the schema and the question to generate the Cypher query and return the response.

    Schema: {schema}
    Question: {question}
    
    NOTE:
    Only return the response and no other details
    """

    cypher_generation_prompt = PromptTemplate(
        template=CYPHER_GENERATION_TEMPLATE,
        input_variables=["schema", "question"],
    )

    cypher_chain = GraphCypherQAChain.from_llm(
        llm,
        graph=neo4j_graph,
        cypher_prompt=cypher_generation_prompt,
        top_k=5,
        verbose=True,
        allow_dangerous_requests=True
    )

    response = cypher_chain.invoke({"query": {"schema": "Product", "question": query_text}})
    print(response["result"])


if __name__ == "__main__":
    # similarity_search()
    #vector_retriever()
    qa_chain()
