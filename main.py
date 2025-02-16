from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout,
    QPushButton, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QPixmap

class DropLabel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            QWidget {
                border: 2px dashed #555;
                background-color: #222;
                border-radius: 10px;
                padding: 20px;
            }
        """)

        # Layout inside drop area
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Container for icon, text, and button
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignCenter)

        # Icon
        self.icon = QLabel()
        pixmap = QPixmap("image.png")  # Load the provided icon
        pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon.setPixmap(pixmap)
        self.icon.setAlignment(Qt.AlignCenter)

        # Text
        self.text_label = QLabel("Drop your file here or browse files")
        self.text_label.setStyleSheet("font-size: 16px; color: #CCCCCC;")
        self.text_label.setAlignment(Qt.AlignCenter)

        # Browse Button inside the drop area
        self.browse_button = QPushButton("Browse Files")
        self.browse_button.setStyleSheet("""
            QPushButton {
                background-color: #FF8800;
                color: white;
                font-size: 16px;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #FFAA33;
            }
        """)
        self.browse_button.clicked.connect(self.browse_file)

        # Add widgets to container layout
        self.container_layout.addWidget(self.icon)
        self.container_layout.addWidget(self.text_label)
        self.container_layout.addWidget(self.browse_button)
        self.container.setLayout(self.container_layout)

        # Add container to main layout
        layout.addWidget(self.container)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.text_label.setText(f"File dropped: {file_path}")

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File")
        if file_path:
            self.text_label.setText(f"Selected: {file_path}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kommverters")
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #111; color: white;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("Kommverters")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #FF8800;")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("The best file Kommpanion")
        subtitle.setStyleSheet("font-size: 14px; color: #888888;")
        subtitle.setAlignment(Qt.AlignCenter)

        # Drop Zone
        self.drop_label = DropLabel()

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.drop_label)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
