from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QFileDialog, QComboBox, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QPixmap
import os

class DropLabel(QWidget):
    def __init__(self, switch_to_convertion_screen, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.switch_to_convertion_screen = switch_to_convertion_screen  # Function to switch screen
        self.uploaded_file_path = ""  # Store full file path

        self.setStyleSheet("""
            QWidget {
                border: 2px dashed #555;
                background-color: #222;
                border-radius: 10px;
            }
        """)
        

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title = QLabel("Kommverters")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 42px; font-weight: bold; color: #FF8800; border:none; background-color: transparent;")

        # Description
        description = QLabel("The best file Kommpanion")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setStyleSheet("font-size: 16px; color: #888; border:none; background-color: transparent; margin-bottom: 20px;")

        # Container for icon
        self.main_container = QWidget()
        self.main_container.setFixedSize(500, 200)
        self.container_layout = QVBoxLayout(self.main_container)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Icon
        self.icon = QLabel()
        pixmap = QPixmap("image.png")  # Load the provided icon
        pixmap = pixmap.scaled(420, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.icon.setPixmap(pixmap)
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon.setStyleSheet("""
            QLabel {
                border: 2px solid transparent;
                border-radius: 10px;
            }
        """)

        # Add widgets to container layout
        self.container_layout.addWidget(self.icon)
        self.main_container.setLayout(self.container_layout)

        # Success message container
        self.success_container = QLabel("File Uploaded")
        self.success_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.success_container.setFixedSize(500, 100)
        self.success_container.setStyleSheet("""
            QWidget {
                border: 2px dashed #555;
                background-color: #222;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        self.success_container.setVisible(False)

        # Add containers to main layout
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(self.main_container)
        layout.addWidget(self.success_container)

    def mousePressEvent(self, event):
        """Trigger browse_file when the container is clicked."""
        self.browse_file()

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File")
        if file_path:
            self.uploaded_file_path = file_path  # Store file path
            self.show_success()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            self.uploaded_file_path = urls[0].toLocalFile()  # Store file path
            self.show_success()

    def show_success(self):
        """Hide main container, show success message, and switch screen."""
        self.main_container.setVisible(False)
        self.success_container.setVisible(True)
        self.switch_to_convertion_screen(self.uploaded_file_path)  # Pass full file path