# Floating AI

Floating AI is a desktop application that utilizes the Groq API to provide AI-powered query responses. It features a user-friendly interface with interactive text input, Markdown-rendered AI responses, and keyboard shortcuts for efficient workflow.

---

## Features

- **AI-powered query responses using the Groq API**: Get instant answers to your questions with the help of the Groq API.
- **Secure environment variable management with .env**: Store your API keys securely using environment variables.
- **Interactive Text Input**: Type your queries or commands in the input box, which clears automatically after submission for a smooth workflow.
- **Markdown-Rendered AI Responses**: View AI-generated replies with Markdown formatting, including headings, bold/italic text, bullet points, and code blocks.
- **Integrated AI-memory**: The AI will remember previous conversations to avoid repetitive queries.
- **Keyboard Shortcuts**:
  - `Enter/Return`: Submit query and get AI response instantly.
  - `Shift + Enter`: Insert a new line in the input box.
  - Type `exit`: Close the application gracefully.
  - Type `clear`: Clear the output display.
  - Type `clear history`: Clear the conversation history.
  - Type `history`: View the conversation history.
  - Type `memory`: View the AI's memory.
  - Type `clear memory`: Clear the AI's memory.
  - Type `set personality: <personality>`: Set the AI's personality.

## Upcoming Features

- **Custom Rules**: Set custom rules for the AI to tailor responses according to your preferences.
- **Improved AI Model**: Integrate more advanced AI models for better response accuracy.
- **Enhanced User Interface**: Implement a more intuitive and user-friendly interface.


---

## Optimizations

- ⚡ **Minimal resource usage** with lightweight UI components
- 🧩 **Modular code structure** for easy maintenance
- ⌨️ **Keyboard shortcuts** for improved workflow efficiency
- 🔒 **Secure .env handling** for API key management
- 📦 **Efficient memory management** for conversation history

---

## Installation

To run the application, ensure you have Python and the required libraries installed.  
You can install the libraries using:

```bash
pip install -r requirements.txt
python3 main.py 
```

## Basic Commands

| Key / Command       | Action                                                  |
|---------------------|---------------------------------------------------------|
| Enter / Return      | Submit query and get AI response instantly.             |
| Shift + Enter       | Insert a new line in the input box.                     |
| F1                  | Copy AI output to clipboard.                            |
| exit                | Close the application gracefully.                       |
| clear               | Clear the output display.                               |
| clear history       | Clear the conversation history.                         |
| history             | View the conversation history.                          |
| memory              | View the AI's memory.                                   |
| clear memory        | Clear the AI's memory.                                  |
| set personality     | Set the AI's personality.                               |

---

## Demo
*(Insert a GIF or link to the demo here)*

---

## Authors
- **@abdullashahzan**

---

## Screenshots
*(Add screenshots or mockups of the UI here)*

---

## FAQ

**Q: How do I run the application?**  
A:  
```bash
python3 main.py
```
**Q: How do I clear the conversation history?**  
A: Type `clear history` in the input box to erase all stored queries and responses.

**Q: Can I erase memory of AI? How can I view stored memory?**  
A: Type `clear memory` in the input box to erase all memory or type `memory` to view stored memory.

**Q: How do I view the conversation history?**  
A: Type `history` in the input box to display all past interactions in the output display.

**Q: How do I my AI a personality?**  
A: Type `set personality: <personality>` in the input box to set your AI chatbot's personality.

**Q: How do I close the application?**  
A: Type `exit` in the input box.

---

## License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
