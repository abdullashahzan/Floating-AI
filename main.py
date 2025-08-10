from Client import ai_response
import sys
import markdown
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextBrowser, QTextEdit
from PyQt5.QtCore import Qt

# Custom CSS for nicer Markdown rendering inside QTextBrowser
CUSTOM_CSS = """
<style>
body {
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    color: #222;
    background: #fff;
    margin: 10px;
}
h1, h2, h3 {
    border-bottom: 1px solid #ddd;
    padding-bottom: 4px;
}
pre {
    background-color: #f5f5f5;
    padding: 8px;
    border-radius: 4px;
    font-family: Consolas, monospace;
    white-space: pre-wrap; /* wrap long code lines */
}
code {
    background-color: #eee;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: Consolas, monospace;
}
ul {
    padding-left: 20px;
}
</style>
"""

def set_markdown_output(output_display: QTextBrowser, md_text: str):
    # Convert Markdown to HTML and add custom CSS
    html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])
    html_with_css = f"<html><head>{CUSTOM_CSS}</head><body>{html}</body></html>"
    output_display.setHtml(html_with_css)

def handle_submit(text_input, output_display):
    query = text_input.toPlainText().strip()
    if query:
        if query.lower() == "exit":
            app.quit()
        else:
            output = str(ai_response(query))
            set_markdown_output(output_display, output)
            text_input.clear()

def copy_output(output_display):
    clipboard = QApplication.clipboard()
    # Copy plain text (rendered) from QTextBrowser to clipboard
    clipboard.setText(output_display.toPlainText())

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Floating AI")
window.resize(600, 400)

layout = QVBoxLayout()

output_display = QTextBrowser()  # QTextBrowser for better HTML rendering
layout.addWidget(output_display)

text_input = QTextEdit()
text_input.setFixedHeight(50)
text_input.setPlaceholderText("Type here...")
layout.addWidget(text_input)

def on_key_press(event):
    if event.key() in (Qt.Key_Return, Qt.Key_Enter):
        handle_submit(text_input, output_display)
    elif event.key() == Qt.Key_Escape:
        app.quit()
    elif event.key() == Qt.Key_F1:
        copy_output(output_display)
    else:
        QTextEdit.keyPressEvent(text_input, event)

text_input.keyPressEvent = on_key_press

window.setLayout(layout)
window.show()
text_input.setFocus()

sys.exit(app.exec_())
