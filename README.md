# Google Gemini Chat Framework
 This Python program uses Google's Gemini Pro API from https://ai.google.dev/ to create the framework for an interactive and configurable chat interface with the Gemini Pro model.
 Users can chat with the model in terminal, as if they were using it on their browser

 ## Features
 * Gemini API Integration
 * Chat History Management: Keeps track of conversation history with a custom `ChatManager` class, allowing for continuity in conversations
 * Persistant Chat Storage: Saves chat history to a custom file, ensuring that the context is preserved even after the program restarts.

## Requirements
* Python 3.x
* Google Gemini API key
* GCloud CLI

## Setup

1. Download the repository or `gemini.py`
2. Install the required packages by running
   ```bash
   python -m pip install google-generativeai python-dotenv
   ```
   or
   
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Setup your GCloud Application default credentials by following [these](https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev) steps. 
4. Setup your `.env` file with your API key.
   
   This can be done by creating a `.env` file in your directory and adding ```GOOGLE_API_KEY = "your_api_key_here"```

## Usage

Run the script with python
```bash
python gemini.py
```
Interact with the bot via the command line, receiving real-time responses

## Commands

- Type messages in the termimal to send to Gemini Pro
- Type 'history' to print the full chat history in the terminal
- Type 'restart' to start a new chat, wipe the bot's history and store to a local file
- Type 'exit' to quit the program and save current session to file

## Contributions

Feel free to fork this project, submit pull requests, or suggest features or improvements via issues.

## License

Project licensed under MIT. See [LICENSE](LICENSE) for more details

**This project is not affiliated with Google, and uses the Gemini API under its respective terms of service.**
