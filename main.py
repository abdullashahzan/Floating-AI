from Client import ai_response
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextBrowser, QTextEdit, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import markdown
from PyQt5.QtCore import Qt

CUSTOM_CSS = """
<style>
body {
    font-family: 'Monaco', monospace;
    font-size: 14px;
}
pre {
    background-color: #333;
    padding: 20px;
    border-radius: 6px;
}
code {
    background-color: #333;
    color: #ddd;
    padding: 4px 6px;
    border-radius: 5px;
}
ul {
    padding-left: 25px;
}
.copy-button {
    color: #fff;
    cursor: pointer;
    border-radius: 5px;
    padding: 5px 10px;
}
</style>
"""

class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ShiftModifier and event.key() == Qt.Key_Return:
            self.insertPlainText('\n')
        elif event.key() == Qt.Key_Return:
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

        self.text_input = CustomTextEdit(self)
        self.text_input.setFixedHeight(50)
        self.text_input.setFocus()
        self.text_input.setPlaceholderText("Type here...")

        self.layout.addWidget(self.text_input)

        self.load_history()

    def set_markdown_output(self, output_display, md_text: str):
        # Convert Markdown to HTML and add custom CSS
        html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])
        copy_button_html = """
        <button class="copy-button" onclick="copySelectedText()">Copy</button>
        <script>
        function copySelectedText() {
            var selectedText = window.getSelection().toString();
            if (selectedText) {
                navigator.clipboard.writeText(selectedText).then(function() {
                    console.log('Text copied to clipboard');
                }, function(err) {
                    console.error('Could not copy text: ', err);
                });
            }
        }
        </script>
        """
        html_with_css = f"<html><head>{CUSTOM_CSS}</head><body>{copy_button_html}{html}</body></html>"
        output_display.setHtml(html_with_css)

    def handle_submit(self):
        query = self.text_input.toPlainText().strip()
        if query:
            if query.lower() == "exit":
                self.close()
            elif query.lower() == "clear":
                self.output_display.clear()
                self.text_input.clear()
            elif query.lower() == "clear history":
                with open("history.txt", "w") as f:
                    f.write("")
                self.load_history()
                self.text_input.clear()
            elif query.lower() == "history":
                self.load_history()
                self.text_input.clear()
            else:
                output = str(ai_response(query))
                self.set_markdown_output(self.output_display, output)
                with open("history.txt", "a") as f:
                    f.write(f"**Query:** {query}\n{output}\n\n")
                self.text_input.clear()

    def load_history(self):
        try:
            with open("history.txt", "r") as f:
                history = f.read()
            self.set_markdown_output(self.output_display, history)
        except FileNotFoundError:
            self.set_markdown_output(self.output_display, "**No conversation history found.**")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())