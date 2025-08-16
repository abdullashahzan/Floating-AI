from Client import ai_response
import sys
import markdown
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTextBrowser,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread
import html
import os, string

CUSTOM_CSS = """
<style>
body {
    font-family: 'Monaco', monospace;
    font-size: 14px;
    color: #e6e6e6;
    margin: 8px;
    padding:10px;
    overflow-wrap: break-word;
}
pre {
    background-color: 'dark gray';
    padding: 12px;
    border-radius: 6px;
    overflow-x: auto;
}
code {
    background-color: 'dark gray';
    color: #000;
    padding: 4px 6px;
    border-radius: 5px;
}
ul {
    padding-left: 25px;
}
</style>
"""

class AIWorker(QObject):
    finished = pyqtSignal(str, str)

    def __init__(self, query):
        super().__init__()
        self.query = query

    def run(self):
        try:
            result = str(ai_response(self.query))
        except Exception as e:
            result = f"**Error:** {str(e)}"
        self.finished.emit(self.query, result)


class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ShiftModifier and event.key() == Qt.Key_Return:
            self.insertPlainText("\n")
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if self.parent:
                self.parent.handle_submit()
        else:
            super().keyPressEvent(event)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Floating AI")
        self.resize(500, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.output_display = QTextBrowser()
        self.output_display.setOpenLinks(False)
        self.layout.addWidget(self.output_display)

        # Copy button
        self.copy_button = QPushButton("Copy Output")
        self.copy_button.clicked.connect(self.copy_output_to_clipboard)
        self.layout.addWidget(self.copy_button)

        self.text_input = CustomTextEdit(self)
        self.text_input.setFixedHeight(70)
        self.text_input.setFocus()
        self.text_input.setPlaceholderText("Type here...")
        self.layout.addWidget(self.text_input)

        # Buttons layout: History, Memory, Personality
        button_layout = QHBoxLayout()
        self.history_button = QPushButton("History")
        self.history_button.clicked.connect(self.load_history)
        button_layout.addWidget(self.history_button)

        self.memory_button = QPushButton("Memory")
        self.memory_button.clicked.connect(self.load_memory_ui)
        button_layout.addWidget(self.memory_button)

        self.personality_button = QPushButton("Personality")
        self.personality_button.clicked.connect(self.set_personality_ui)
        button_layout.addWidget(self.personality_button)

        self.layout.addLayout(button_layout)

        self._worker_thread = None
        self._worker = None

        # Ensure features directory exists
        os.makedirs("features", exist_ok=True)

        self.set_markdown_output(self.output_display, "Hey, there! How can I help you today?")


    def copy_output_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output_display.toPlainText())

    def set_markdown_output(self, output_display, md_text: str):
        try:
            html_content = markdown.markdown(
                md_text, extensions=["fenced_code", "codehilite"]
            )
        except Exception:
            html_content = f"<pre>{html.escape(md_text)}</pre>"

        html_with_css = f"<html><head>{CUSTOM_CSS}</head><body>{html_content}</body></html>"
        output_display.setHtml(html_with_css)

    def analyze_text(self, user_text):
        important_keywords = ["remember", "note", "important", "save", "store"]
        lowered = user_text.lower()
        try:
            with open("features/memory.txt", "r", encoding="utf-8") as f:
                current_memory = f.read()
        except FileNotFoundError:
            current_memory = ""
        if any(keyword in lowered for keyword in important_keywords):
            self.save_to_memory(user_text.strip())
            return user_text.strip()
        if user_text.strip().endswith("?") or len(user_text.split()) > 6:
            self.save_to_memory(user_text.strip())
            return user_text.strip()
        return None

    def save_to_memory(self, text):
        with open("features/memory.txt", "a", encoding="utf-8") as f:
            f.write(text + "\n")

    def load_memory(self):
        try:
            with open("features/memory.txt", "r", encoding="utf-8") as f:
                memory = f.read()
            if not memory.strip():
                return "**Memory is empty.**"
            return memory
        except FileNotFoundError:
            return "**Memory file not found.**"

    def clear_memory(self):
        try:
            with open("features/memory.txt", "w", encoding="utf-8") as f:
                f.write("")
        except Exception as e:
            print(f"Error clearing memory: {e}")

    def load_memory_ui(self):
        memory_content = self.load_memory()
        self.set_markdown_output(self.output_display, memory_content)

    def set_personality_ui(self):
        try:
            with open("features/personality.txt", "r", encoding="utf-8") as f:
                personality = f.read()
        except FileNotFoundError:
            personality = "**No personality set.**"
        self.set_markdown_output(self.output_display, personality)

    def handle_submit(self):
        query = self.text_input.toPlainText().strip()
        if not query:
            return

        lower_q = query.lower()
        if lower_q == "exit":
            self.close()
            return

        if lower_q == "clear":
            self.output_display.clear()
            self.text_input.clear()
            return

        if lower_q == "clear history":
            try:
                with open("features/history.txt", "w", encoding="utf-8") as f:
                    f.write("")
            except Exception as e:
                print(f"Error clearing history: {e}")
            self.load_history()
            self.text_input.clear()
            return

        if lower_q == "history":
            self.load_history()
            self.text_input.clear()
            return

        if lower_q == "memory":
            self.load_memory_ui()
            self.text_input.clear()
            return

        if lower_q == "clear memory":
            self.clear_memory()
            self.set_markdown_output(self.output_display, "**Memory cleared successfully.**")
            self.text_input.clear()
            return
            
        if lower_q == "clear all":
            try:
                with open("features/history.txt", "w", encoding="utf-8") as f:
                    f.write("")
                with open("features/memory.txt", "w", encoding="utf-8") as f:
                    f.write("")
            except Exception as e:
                print(f"Error clearing all: {e}")
            self.load_history()
            self.set_markdown_output(self.output_display, "**All cleared successfully.**")
            self.text_input.clear()
            return

        if lower_q.startswith("set personality:"):
            parts = query.split(":", 1)
            if len(parts) > 1:
                personality_settings = parts[1].strip()
                try:
                    with open("features/personality.txt", "w", encoding="utf-8") as f:
                        f.write(personality_settings)
                    self.set_markdown_output(self.output_display, "**Personality settings saved successfully!**")
                except Exception as e:
                    self.set_markdown_output(self.output_display, f"**Error saving personality:** {e}")
            else:
                self.set_markdown_output(self.output_display, "**Error: No personality provided.**")
            self.text_input.clear()
            return

        try:
            content_to_save = self.analyze_text(query)
            if content_to_save is not None:
                try:
                    with open("features/memory.txt", "w", encoding="utf-8") as f:
                        f.write(content_to_save)
                except Exception as e:
                    print(f"Error writing memory: {e}")
        except Exception as e:
            print(f"Error analyzing or saving memory: {e}")

        self.set_markdown_output(self.output_display, "**Loading response...**")
        self.text_input.clear()

        worker = AIWorker(query)
        thread = QThread()
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(self.on_ai_response)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)

        self._worker_thread = thread
        self._worker = worker
        thread.start()

    def on_ai_response(self, query: str, output: str):
        self.set_markdown_output(self.output_display, output)
        try:
            with open("features/history.txt", "a", encoding="utf-8") as f:
                query = query.lower().translate(str.maketrans("", "", string.punctuation))
                query = " ".join(query.split())
                output = output.lower().translate(str.maketrans("", "", string.punctuation))
                output = " ".join(output.split())
                f.write(f"User: {query} Your response: {output}")
        except Exception as e:
            print(f"Error saving history: {e}")

    def load_history(self):
        try:
            with open("features/history.txt", "r", encoding="utf-8") as f:
                history = f.read()
                self.set_markdown_output(self.output_display, history)
        except FileNotFoundError:
            self.set_markdown_output(self.output_display, "**No conversation history found.**")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
