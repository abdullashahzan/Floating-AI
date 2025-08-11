from Client import ai_response
import sys
import markdown
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTextBrowser,
    QTextEdit,
    QPushButton
)
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread
import html
import os

CUSTOM_CSS = """
<style>
body {
    font-family: 'Monaco', monospace;
    font-size: 14px;
    color: #e6e6e6;
    margin: 8px;
}
pre {
    background-color: #111;
    padding: 12px;
    border-radius: 6px;
    overflow-x: auto;
}
code {
    background-color: #111;
    color: #ddd;
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

        # --- NEW: Real Copy Button ---
        self.copy_button = QPushButton("Copy Output")
        self.copy_button.clicked.connect(self.copy_output_to_clipboard)
        self.layout.addWidget(self.copy_button)

        self.text_input = CustomTextEdit(self)
        self.text_input.setFixedHeight(70)
        self.text_input.setFocus()
        self.text_input.setPlaceholderText("Type here...")
        self.layout.addWidget(self.text_input)

        self._worker_thread = None
        self._worker = None

        self.load_history()

    def copy_output_to_clipboard(self):
        """Copies the plain text of the output display to clipboard."""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output_display.toPlainText())

    def set_markdown_output(self, output_display, md_text: str):
        safe_md = md_text
        try:
            html_content = markdown.markdown(safe_md, extensions=["fenced_code", "codehilite"])
        except Exception:
            html_content = f"<pre>{html.escape(safe_md)}</pre>"

        html_with_css = f"<html><head>{CUSTOM_CSS}</head><body>{html_content}</body></html>"
        output_display.setHtml(html_with_css)

    def analyze_text(self, text):
        important_keywords = ["remember", "note", "important", "save", "store"]
        lowered = text.lower()
        for keyword in important_keywords:
            if keyword in lowered:
                return True
        stripped = text.strip()
        if stripped.endswith("?") or len(stripped.split()) > 6:
            return True
        return False

    def save_to_memory(self, key, text):
        try:
            os.makedirs(os.path.dirname("features/memory.txt"), exist_ok=True)
        except Exception:
            pass
        try:
            with open("features/memory.txt", "a", encoding="utf-8") as f:
                f.write(f"## {key}\n{text}\n\n")
        except Exception:
            pass

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
        except Exception:
            pass

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
            except Exception:
                pass
            self.load_history()
            self.text_input.clear()
            return

        if lower_q == "history":
            self.load_history()
            self.text_input.clear()
            return

        if lower_q == "memory":
            memory_content = self.load_memory()
            self.set_markdown_output(self.output_display, memory_content)
            self.text_input.clear()
            return

        if lower_q == "clear memory":
            self.clear_memory()
            self.set_markdown_output(self.output_display, "**Memory cleared successfully.**")
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
                except Exception:
                    self.set_markdown_output(self.output_display, "**Error saving personality.**")
            else:
                self.set_markdown_output(self.output_display, "**Error: No personality provided.**")
            self.text_input.clear()
            return

        try:
            if self.analyze_text(query):
                self.save_to_memory("important_text", query)
        except Exception:
            pass

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
                f.write(f"**Query:** {query}\n{output}\n\n")
        except Exception:
            pass

    def load_history(self):
        try:
            with open("features/history.txt", "r", encoding="utf-8") as f:
                history = f.read()
            if not history.strip():
                self.set_markdown_output(self.output_display, "**No conversation history found.**")
            else:
                self.set_markdown_output(self.output_display, history)
        except FileNotFoundError:
            self.set_markdown_output(self.output_display, "**No conversation history found.**")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
