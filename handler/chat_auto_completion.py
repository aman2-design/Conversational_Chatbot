from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate


embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
faiss_index_path = r"C:\Users\amani\OneDrive\Desktop\Virtual_Assistant\faiss_index.bin"

final_vectors = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)

llm = OllamaLLM(model="gemma")

prompt_template = """
User has entered a partial query {partial_query} 

Using the context provided below, generate three possible full questions that the user might ask 
starting with the {partial_query} words.

Context from the database:
{faiss_context}

Provide three distinct and relevant questions that align with the user's partial query and the given context.
"""

# Create the PromptTemplate object
prompt = PromptTemplate(input_variables=["partial_query","faiss_context"], template=prompt_template)


# Set up LLMChain
chain = prompt | llm

def auto_complete(user_partial_query):
    faiss_context = final_vectors.similarity_search(user_partial_query,k = 1)
    faiss_context_1 = " ".join([i.page_content for i in faiss_context])
    response = chain.invoke(input={"partial_query":user_partial_query,"faiss_context":faiss_context_1})
    return response

#auto_complete("What is my ins")


