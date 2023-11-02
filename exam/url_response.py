import sys
import requests
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QTextEdit,
    QListWidget,
    QLabel,
)


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Http APP")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        
        self.label = QLabel("Enter URL:", self)
        self.layout.addWidget(self.label)
        
        
        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        self.status_label = QLabel("", self)
        self.layout.addWidget(self.status_label)

        self.status_text = QTextEdit(self)
        self.status_text.setReadOnly(True)
        self.layout.addWidget(self.status_text)

        self.request_button = QPushButton("Send request", self)
        self.request_button.clicked.connect(self.send_request)
        self.layout.addWidget(self.request_button)

    def send_request(self):
        self.status_label.setText("Response")

        url = self.text_edit.toPlainText()
        try:
            response = requests.get(url)
            status_code = response.status_code
            status_text = response.reason

            self.status_text.setText(
                f"Status code: {status_code}\nStatus Text: {status_text}\n"
            )
        except Exception as e:
            self.status_text.setText(f"{str(e)}")
            self.status_label.setText(f"Error:")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
