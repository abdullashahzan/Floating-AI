# Floating AI

Floating AI is a desktop application that utilizes the Groq API to provide AI-powered query responses. It features a user-friendly interface with interactive text input, Markdown-rendered AI responses, and keyboard shortcuts for efficient workflow.

---

## Features

- **AI-powered query responses using the Groq API**: Get instant answers to your questions with the help of the Groq API.  
- **Secure environment variable management with `.env`**: Store your API keys securely using environment variables.  
- **Interactive Text Input**: Type your queries or commands in the input box, which clears automatically after submission for a smooth workflow.  
- **Markdown-Rendered AI Responses**: View AI-generated replies with Markdown formatting, including headings, bold/italic text, bullet points, and code blocks.  

### Keyboard Shortcuts:
- **Enter/Return**: Submit query and get AI response instantly.  
- **Shift + Enter**: Insert a new line in the input box.  
- **Type `exit`**: Close the application gracefully.  
- **Type `clear`**: Clear the output display.  
- **Type `clear history`**: Clear the conversation history.  
- **Type `history`**: View the conversation history.

- **Copy Button**: Copy the AI output text to the clipboard with a single click.  

- **Integrated AI-memory**: The AI will remember previous conversations to avoid repetitive queries.  


---

## Upcoming Features

- **Custom Rules**: Set custom rules for the AI to tailor responses according to your preferences.  


---

## Installation

To run the application, ensure you have Python and the required libraries installed.  
You can install the libraries using:

```bash
pip install -r requirements.txt
python3 main.py 
```

### Basic Commands

| Key / Command   | Action                                           |
|-----------------|--------------------------------------------------|
| **Enter / Return** | Submit query and get AI response instantly.     |
| **Shift + Enter**  | Insert a new line in the input box.              |
| **F1**             | Copy AI output to clipboard.                    |
| **exit**           | Close the application gracefully.               |
| **clear**          | Clear the output display.                        |
| **clear history**  | Clear the conversation history.                  |
| **history**        | View the conversation history.                   |

---

## Demo
*(Insert a GIF or link to the demo here)*

---

## Authors
- **Your GitHub Username**

---

## Documentation
*(Add a link to detailed documentation if available)*

---

## Screenshots
*(Add screenshots or mockups of the UI here)*

---

## Optimizations
- Minimal resource usage with lightweight UI components.  
- Consistent coding style for easy maintainability.  
- Keyboard shortcuts for improved efficiency.  
- Secure `.env` file handling for API keys.  

---

## FAQ

**Q: How do I run the application?**  
A:  
```bash
python main.py
```
**Q: How do I clear the conversation history?**  
A: Type `clear history` in the input box to erase all stored queries and responses.

**Q: How do I view the conversation history?**  
A: Type `history` in the input box to display all past interactions in the output display.

**Q: How do I copy the AI output?**  
A: Press `F1` on your keyboard to instantly copy the latest AI response to your clipboard.

**Q: How do I close the application?**  
A: Type `exit` in the input box or press the `Esc` key.

---

## License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
