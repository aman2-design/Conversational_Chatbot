
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from handler.chat_history_buffer import get_chat_history
from langchain.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
llm = OllamaLLM(model="gemma")


embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
faiss_index_path = r"C:\Users\amani\OneDrive\Desktop\Virtual_Assistant\faiss_index.bin"


final_vectors = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)


def get_answer(user_question,user_id,chat_history):

    previous_conversation = get_chat_history(chat_history,user_id)
    user_updated_query = " ".join(previous_conversation) + " " + user_question
    response = final_vectors.similarity_search(user_updated_query,k = 1)
    for result in response:
        faiss_response = result.page_content

    new_prompt = """You are an expert conversational assistant. Based on the question {user_updated_query} 
    and the response {response}, summarize and refine the answer into a more concise, human-readable, and 
    conversational format. Ensure the response is clear, engaging, and uses minimal words while maintaining the 
    essence of the original answer.
    """

    prompt_structure = PromptTemplate(input_variables=["user_updated_query","response"], template = new_prompt)


    chain = prompt_structure | llm
    human_response = chain.invoke(input = {"user_updated_query":user_updated_query,"response":faiss_response})    


    if human_response:
        return human_response
    else:
        return "Sorry, I can't able to find answer of this question"  




