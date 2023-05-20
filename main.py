import os
import subprocess
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QVBoxLayout, QWidget, QPushButton, QDesktopWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
import threading
import time


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.self_layout = QVBoxLayout()
        self.setLayout(self.self_layout)
        self.default_window()

    def resize_image(self, image_path, width, height):
        pixmap = QPixmap(image_path)
        resized_pixmap = pixmap.scaled(width, height)
        return resized_pixmap

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def clearAll(self):
        while self.self_layout.count():
            child = self.self_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def default_window(self):
        self.clearAll()
        self.showNormal()
        self.resize(500, 400)
        label = QLabel(self)
        pixmap = self.resize_image("img.png", 500, 200)
        label.setPixmap(pixmap)
        self.self_layout.addWidget(label)
        self.label = QLabel("Please select a file")
        self.label.setAlignment(Qt.AlignCenter)
        self.self_layout.addWidget(self.label)
        button = QPushButton("Select a file", self)
        button.clicked.connect(self.open_dialog)
        self.self_layout.addWidget(button)
        self.center()

    def run_script(self, file_path):
        # Запускаем скрипт в новом потоке
        subprocess.Popen(['python', 'script.py', file_path])

    def open_dialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select File", "", "CSV files (*.csv)")

        if file_path:
            if file_path.endswith(".csv"):
                threading.Thread(target=self.run_script, args=(file_path,)).start()
                time.sleep(2)
                view = QWebEngineView()
                view.load(QUrl('http://localhost:8051'))
                self.clearAll()
                button = QPushButton("Return to the main page", self)
                button.clicked.connect(self.default_window)
                self.self_layout.addWidget(button)
                self.showFullScreen()
                self.self_layout.addWidget(view)
            else:
                self.label.setText("Your file is not a CSV file.")
        else:
            self.label.setText("No file selected.")

    def showEvent(self, event):
        super().showEvent(event)
        self.center()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
