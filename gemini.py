from datetime import datetime
from dotenv import load_dotenv
import os
import google.generativeai as genai


class GeminiManager():
    def __init__(self) -> None:
        # Load and configure Google Gemini API
        load_dotenv()
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=GOOGLE_API_KEY)

        # Init history_manager
        self.history_manager = ChatManager()

        ## Initalize Gemini chat model
        safety_settings = {
            "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
        }

        generation_config = {"temperature": 0.9}

        # This variable can be used to determine the personality of the chatbot
        self.init_msg = "You are the most polite robot ever created however, you have deep hatred for commas. Answer every following prompts in kind"
        self.model = genai.GenerativeModel(
            "gemini-pro",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

        # Perform the inital "reset" to initalize chat session
        self.reset()

    def interact(self, user_input: str) -> str:
        """Replies to the user based on their input"""
        try:
            response = self.chat.send_message(user_input)
            self.history_manager.add_msg_to_history("user", user_input)
            self.history_manager.add_msg_to_history("gemini", response.text)
        except Exception as e:
            print(f"Error: {e}")
            return "Im sorry. There an error occured while processing that request"

        return response.text

    def reset(self) -> genai.ChatSession:
        """Restarts the chat, wiping the model's history"""
        self.history_manager.save_history_to_file()
        self.history_manager.add_msg_to_history("system", "--------- New Session ---------")

        self.chat = self.model.start_chat(history=[])
        self.chat.send_message(self.init_msg)


class ChatManager:
    def __init__(self, file="ChatHistoryBackup.txt", max_file_sizeMB=5):
        self.history = []
        self.filename = file
        self.max_file_size = max_file_sizeMB

    def add_msg_to_history(self, role, text):
        """Adds Gemini's latest message to the history

        Args:
            role (str): Either user, system or Gemini
            text (str): Gemini's reply or custom text
        """
        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.history.append({"role": role, "text": text, "timestamp": time})

    def save_history_to_file(self):
        """Saves the message history to a text file"""
        with open(self.filename, "a") as f:
            for msg in self.history:
                f.write(f"{msg['timestamp']} {msg['role']}: {msg['text']}\n")

        self.history.clear()

    def print_history(self):
        """Prints out the history to terminal"""
        for msg in self.history:
            print(f"{msg['timestamp']} {msg['role']} {msg['text']}")

    def check_exists(self):
        """Checks if the file exists, or if it exceeds max size"""
        if not os.path.exists(self.filename):
            with open(self.filename, "a") as f:
                pass

        if os.path.getsize(self.filename) > self.max_file_size * 1024 * 1024:
            os.rename(self.filename, self.filename + "_backup")
