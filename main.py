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
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Container for icon, text, and button
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
        # transparent border
        self.icon.setStyleSheet("""
            QLabel {
                border: 2px solid transparent;
                border-radius: 10px;
            }
        """)

        # Add widgets to container layout
        self.container_layout.addWidget(self.icon)
        self.main_container.setLayout(self.container_layout)

        # Success message container (initially hidden)
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
        layout.addWidget(self.main_container)
        layout.addWidget(self.success_container)

    def mousePressEvent(self, event):
        """Trigger browse_file when the container is clicked."""
        self.browse_file()

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File")
        if file_path:
            self.show_success()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.show_success()

    def show_success(self):
        """Hide main container and show success message."""
        self.main_container.setVisible(False)
        self.success_container.setVisible(True)

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
