import sys
import json
import os
from PyQt6.QtWidgets import (
    QWidget, QApplication, QLineEdit, 
    QPushButton, QFormLayout
)

CONFIG_FILE = "config.json"

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Настройки")
        self.resize(400, 150)
        
        layout = QFormLayout()
        self.setLayout(layout)

        self.threads_input = QLineEdit()
        self.chat_input = QLineEdit()
        
        layout.addRow("Threads Link:", self.threads_input)
        layout.addRow("ChatGPT Link:", self.chat_input)

        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.save_settings)
        layout.addRow(save_btn)

        self.load_settings()

    def load_settings(self):
        default_threads = "https://www.threads.com/"
        default_chat = "https://chatgpt.com/"
        
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.threads_input.setText(data.get("threads_url", default_threads))
                    self.chat_input.setText(data.get("chat_url", default_chat))
            except:
                self.threads_input.setText(default_threads)
                self.chat_input.setText(default_chat)
        else:
            self.threads_input.setText(default_threads)
            self.chat_input.setText(default_chat)

    def save_settings(self):
        data = {
            "threads_url": self.threads_input.text().strip(),
            "chat_url": self.chat_input.text().strip()
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec())