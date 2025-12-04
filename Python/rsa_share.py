import json
import os

# Filepath for storing the session data
SESSION_FILE = "rsa_session.json"

def save_session_data(session_data):
    """
    Save session data (like RSA keys and ciphertext) to a JSON file.
    
    Args:
        session_data (dict): Dictionary containing RSA-related data.
    """
    try:
        with open(SESSION_FILE, "w") as file:
            json.dump(session_data, file, indent=4)
        print(f"Session data saved to {SESSION_FILE}.")
    except Exception as e:
        print(f"Error saving session data: {e}")

def load_session_data():
    """
    Load session data (like RSA keys and ciphertext) from a JSON file.
    
    Returns:
        dict: Dictionary containing the loaded session data.
    """
    if not os.path.exists(SESSION_FILE):
        print(f"Session file {SESSION_FILE} not found. Returning an empty dictionary.")
        return {}
    
    try:
        with open(SESSION_FILE, "r") as file:
            session_data = json.load(file)
        print(f"Session data loaded from {SESSION_FILE}.")
        return session_data
    except Exception as e:
        print(f"Error loading session data: {e}")
        return {}
