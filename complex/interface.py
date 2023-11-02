import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QTextEdit,
    QListWidget,
)
from PyQt6.QtCore import QTimer, Qt
import requests

class TaskClient(QMainWindow):
    def __init__(self):
        super(TaskClient, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Task Client")
        self.setGeometry(100, 100, 400, 400) 

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.task_list = QListWidget(self)
        layout.addWidget(self.task_list)

        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)

        self.description_text_edit = QTextEdit(self)  
        layout.addWidget(self.description_text_edit)

        self.add_task_button = QPushButton("Add Task", self)
        self.add_task_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_task_button)

        self.delete_task_button = QPushButton("Delete Task", self)
        self.delete_task_button.clicked.connect(self.delete_task)
        layout.addWidget(self.delete_task_button)

        self.central_widget.setLayout(layout)

        self.load_tasks() 


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_tasks)
        self.timer.start(5000)  

        self.task_list.itemClicked.connect(self.show_description)

    def add_task(self):
        task_text = self.text_edit.toPlainText()
        description = self.description_text_edit.toPlainText()
        if task_text:
            try:
                response = requests.post("http://127.0.0.1:5000/add_task", data={"task": task_text, "description": description})
                if response.status_code == 200:
                    self.text_edit.clear()
                    self.description_text_edit.clear() 
            except Exception as e:
                print(f"Error: {str(e)}")

    def delete_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            task_text = selected_item.text()
            try:
                response = requests.post("http://127.0.0.1:5000/delete_task", data={"task": task_text})
                if response.status_code == 200:
                    self.load_tasks()
            except Exception as e:
                print(f"Error: {str(e)}")

    def show_description(self, item):
        selected_task = item.text()
        self.description_text_edit.clear()
        try:
            response = requests.get("http://127.0.0.1:5000/get_tasks_json")
            if response.status_code == 200:
                tasks = response.json()
                for task in tasks:
                    if task["task"] == selected_task:
                        description = task["description"]
                        if description:
                            self.description_text_edit.setPlainText(description)
                        else:
                            self.description_text_edit.setPlainText("No available description")
                        return
        except Exception as e:
            print(f"Error: {str(e)}")


    def load_tasks(self):
        try:
            response = requests.get("http://127.0.0.1:5000/get_tasks_json")
            if response.status_code == 200:
                tasks = response.json()
                self.task_list.clear()
                for task in tasks:
                    self.task_list.addItem(task["task"])
        except Exception as e:
            print(f"Error: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = TaskClient()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
