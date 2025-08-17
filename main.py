# main.py
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
import os
import string
import subprocess


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
    background-color: #2e2e2e;
    padding: 12px;
    border-radius: 6px;
    overflow-x: auto;
}
code {
    background-color: #2e2e2e;
    color: #f8f8f2;
    padding: 4px 6px;
    border-radius: 5px;
}
ul {
    padding-left: 25px;
}
</style>
"""

# -----------------------------
# Worker
# -----------------------------
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


# -----------------------------
# Custom Text Box
# -----------------------------
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


# -----------------------------
# Main Window
# -----------------------------
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

        # Buttons layout: History, Personality
        button_layout = QHBoxLayout()

        self.history_button = QPushButton("History")
        self.history_button.clicked.connect(self.load_history)
        button_layout.addWidget(self.history_button)

        self.personality_button = QPushButton("Personality")
        self.personality_button.clicked.connect(self.set_personality_ui)
        button_layout.addWidget(self.personality_button)

        self.layout.addLayout(button_layout)

        self._worker_thread = None
        self._worker = None

        # Ensure features directory exists
        os.makedirs("features", exist_ok=True)

        self.set_markdown_output(self.output_display, "Hey, there! How can I help you today?")

    # -----------------------------
    # Utility Functions
    # -----------------------------
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

    def save_to_memory(self, text):
        cleaned = text.lower()
        cleaned = cleaned.translate(str.maketrans("", "", string.punctuation))
        cleaned = " ".join(cleaned.split())  # remove newlines/extra spaces
        with open("features/memory.txt", "a", encoding="utf-8") as f:
            f.write(cleaned + " ")

    def load_history(self):
        try:
            with open("features/history.txt", "r", encoding="utf-8") as f:
                history = f.read()
                self.set_markdown_output(
                    self.output_display,
                    history if history.strip() else "**History is empty.**",
                )
        except FileNotFoundError:
            self.set_markdown_output(self.output_display, "**No conversation history found.**")

    def set_personality_ui(self):
        file_path = "features/personality.txt"
        try:
            if sys.platform.startswith("win"):
                os.startfile(file_path)
            elif sys.platform.startswith("darwin"):
                subprocess.call(["open", file_path])
            else:
                subprocess.call(["xdg-open", file_path])
        except Exception as e:
            self.set_markdown_output(self.output_display, f"**Error opening personality file:** {e}")

    # -----------------------------
    # Main Handlers
    # -----------------------------
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
            self.set_markdown_output(self.output_display, "**History cleared. ✅**")
            self.text_input.clear()
            return

        if lower_q == "clear memory":
            try:
                with open("features/memory.txt", "w", encoding="utf-8") as f:
                    f.write("")
            except Exception as e:
                print(f"Error clearing memory: {e}")
            self.set_markdown_output(self.output_display, "**Memory cleared. ✅**")
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
            self.output_display.clear()
            self.set_markdown_output(self.output_display, "**All history and memory cleared. ✅**")
            self.text_input.clear()
            return

        if lower_q == "history":
            self.load_history()
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

        # Save to memory (compact form)
        self.save_to_memory(f"User: {query}")

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
            # Save full history (human readable)
            with open("features/history.txt", "a", encoding="utf-8") as f:
                f.write(f"User: {query}\n\n#AI: {output}\n\n")
        except Exception as e:
            print(f"Error saving history: {e}")

        # Save compact memory version
        self.save_to_memory(f"AI: {output}")


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
