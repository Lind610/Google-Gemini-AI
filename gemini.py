from datetime import datetime
from dotenv import load_dotenv
import os
import google.generativeai as genai

class ChatHistoryManager:
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
    self.history.append(
      {'role': role, 'text': text, 'timestamp': time}
    )
  
  def save_history_to_file(self):
    """Saves the message history to a text file
    """
    with open(self.filename, 'a') as f:
      for msg in self.history:
        f.write(f"{msg['timestamp']} {msg['role']}: {msg['text']}\n")
        
    self.history.clear()
  
  
  def print_history(self):
    """Prints out the history to terminal
    """
    for msg in self.history:
      print(f"{msg['timestamp']} {msg['role']} {msg['text']}")
  
  
  def check_exists(self):
    """Checks if the file exists, or if it exceeds max size
    """
    if not os.path.exists(self.filename):
      with open(self.filename, 'a') as f:
        pass
    
    if os.path.getsize(self.filename) > self.max_file_size * 1024 * 1024:
      os.rename(self.filename, self.filename + "_backup")


load_dotenv()

# This is the file that the chat history will be saved to
BACKUP_FILE = "ChatHistoryBackup.txt"

# This is a setting that will determine the first message passed to the API
FIRST_SYSTEM_MSG = '''ENTER INSTRUCTIONS HERE, THAT WILL BE PASSED AS THE 1ST MESSAGE TO GEMINI
FOR EXAMPLE, "YOU ARE CAPTAIN JACK SPARROW, FAMOUS PIRATE! ANSWER QUESTIONS IN HIS STYLE'''

# Get the API key from the .env Make sure to set this up
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Modifiying the model config so messages aren't blocked
safety_settings = {
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
}

# Change the config to determine the outputs of the model
generation_config = {
  "temperature": 0.9
}

# Creating new instance of the history manager and creating initial session message
history_manager = ChatHistoryManager()
history_manager.add_msg_to_history("system", "----New Session----")

# Selecting the model to use and initialising it
model = genai.GenerativeModel('gemini-pro', safety_settings=safety_settings, generation_config=generation_config)
chat = model.start_chat(history=[])
chat

# Passing the first message in, without displaying the response. Which can optionally be viewed
response = chat.send_message(FIRST_SYSTEM_MSG)
#print(response.text)
print("----------------------------------------")

# Main loop
while True:
  user_input = input("Awaiting input. What would you like to do?")
  print("----------------------------------------")
  
  # If user types 'exit', quits the program and saves the char history 
  if user_input.lower() == "exit":
    history_manager.save_history_to_file()
    break
  
  # Views the chat history
  elif user_input.lower() == "history":
    history_manager.print_history()
    continue
  
  # Restarts the chat, wiping the model's history
  elif user_input.lower() == "restart":
    history_manager.save_history_to_file()
    os.system('cls' if os.name == 'nt' else 'clear')
    history_manager.add_msg_to_history("system", "----New Session----")
    chat = model.start_chat(history=[])
    continue
  
  # Replies to the user based on their input
  try:
    response = chat.send_message(user_input)
    print(response.text)
    history_manager.add_msg_to_history("user", user_input)
    history_manager.add_msg_to_history("gemini", response.text)
  except Exception as e:
            print(f"An error occurred: {e}")