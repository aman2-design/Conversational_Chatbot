from flask import Flask, request, jsonify
from handler.faq_generation import get_answer
from handler.chat_auto_completion import auto_complete
from handler.chat_history_buffer import update_chat_history, get_chat_history,clear_chat_history
from flask import render_template




app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

chat_history = {}


@app.route("/conversational_faq",methods = ['POST'])
def conversational_faq():
    user_id = request.headers.get("User-ID")
    data = request.get_json()
    question = data.get("question")
    
    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Update chat history with the new question
    update_chat_history(chat_history, user_id, question)

    # Generate the FAQ answer with chat history context
    faq_answer = get_answer(question, user_id, chat_history)
    formatted_response = faq_answer.replace("\n", "<br>")
    
    return {"answer": formatted_response}

@app.route("/auto_text",methods = ['POST'])
def auto_text():
    data = request.get_json()
    partial_question = data.get("partial_query")
    if not partial_question:
        return jsonify({"error": "No query provided"}), 400

    completed_query = auto_complete(partial_question)
    formatted_response = completed_query.replace("\n", "<br>")
    return {"completed_query": formatted_response}

if __name__ == "__main__":
    app.run(debug=True)
