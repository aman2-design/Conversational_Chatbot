# Update chat history for the user
def update_chat_history(history_dict, user_id, user_input):
    """
    Appends the user input to the chat history for the given user_id.
    """
    if user_id not in history_dict:
        history_dict[user_id] = []
    
    history_dict[user_id].append(user_input)

# Retrieve chat history for the user
def get_chat_history(history_dict, user_id):
    """
    Retrieves the chat history for the given user_id.
    """
    if user_id in history_dict:
        return history_dict[user_id]
    else:
        return []

# Clear chat history for the user
def clear_chat_history(history_dict, user_id):
    """
    Clears the chat history for the given user_id.
    """
    if user_id in history_dict:
        del history_dict[user_id]