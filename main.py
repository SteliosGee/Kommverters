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
                padding: 20px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

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


class ConvertionScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversion Screen")
        self.setStyleSheet("background-color: #111; color: white;")

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("You are on the Conversion Screen")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # New wrapper layout with pink background
        self.wrapper_layout = QVBoxLayout()
        self.wrapper_container = QWidget()
        self.wrapper_container.setStyleSheet("background-color: #222; border-radius: 10px; padding: 10px;")
        self.wrapper_container.setLayout(self.wrapper_layout)

        self.file_display_layout = QHBoxLayout()
        self.file_display_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.image_preview = QLabel()
        self.file_name_label = QLabel("")
        self.file_name_label.setStyleSheet("font-size: 16px; color: #FF8800;")

        self.file_display_layout.addWidget(self.image_preview)
        self.file_display_layout.addWidget(self.file_name_label)

        self.output_layout = QHBoxLayout()
        self.output_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.format_layout = QVBoxLayout()
        self.format_label = QLabel("Format:")
        self.format_label.setStyleSheet("color: #002eff; font-size: 15px; margin-bottom: -14px; margin-left: -10px;")
        self.desired_format = QComboBox()
        self.desired_format.addItems(["PNG", "JPG", "BMP", "GIF"])
        self.desired_format.setStyleSheet("background-color: #333; color: white;")
        self.format_layout.addWidget(self.format_label)
        self.format_layout.addWidget(self.desired_format)

        self.output_name_layout = QVBoxLayout()
        self.output_name_label = QLabel("Output Name:")
        self.output_name_label.setStyleSheet("color: #002eff; font-size: 15px; margin-bottom: -14px; margin-left: -10px;")
        self.output_name = QLineEdit()
        self.output_name.setStyleSheet("background-color: #333; color: white;")
        self.output_name_layout.addWidget(self.output_name_label)
        self.output_name_layout.addWidget(self.output_name)

        self.size_layout = QVBoxLayout()
        self.size_label = QLabel("Size:")
        self.size_label.setStyleSheet("color: #002eff; font-size: 15px; margin-bottom: -14px; margin-left: -10px;")
        self.size_combo = QComboBox()
        self.size_combo.addItems(["Small", "Medium", "Large"])
        self.size_combo.setStyleSheet("background-color: #333; color: white;")
        self.size_layout.addWidget(self.size_label)
        self.size_layout.addWidget(self.size_combo)

        self.output_layout.addLayout(self.format_layout)
        self.output_layout.addLayout(self.output_name_layout)
        self.output_layout.addLayout(self.size_layout)

        # Add layouts inside the pink wrapper
        self.wrapper_layout.addLayout(self.file_display_layout)
        self.wrapper_layout.addLayout(self.output_layout)

        # Add widgets to the main layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.wrapper_container)  # Add the pink container
        self.setLayout(self.layout)


    def set_file(self, file_path):
        """Update UI with file name and image preview (if applicable)."""
        file_name = os.path.basename(file_path)
        self.file_name_label.setText(file_name)

        # Check if the file is an image
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                self.image_preview.setPixmap(pixmap)
        else:
            self.image_preview.clear()  # Clear image preview for non-image files


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kommverters")
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #111; color: white;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("Kommverters")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #FF8800;")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("The best file Kommpanion")
        subtitle.setStyleSheet("font-size: 14px; color: #888888;")
        subtitle.setAlignment(Qt.AlignCenter)

        # Drop Zone
        self.drop_label = DropLabel(self.show_convertion_screen)

        self.layout.addWidget(title)
        self.layout.addWidget(subtitle)
        self.layout.addWidget(self.drop_label)

        # Create conversion screen
        self.convertion_screen = ConvertionScreen()

    def show_convertion_screen(self, file_path):
        """Switch to the conversion screen and display file details."""
        self.convertion_screen.set_file(file_path)
        self.setCentralWidget(self.convertion_screen)
        self.convertion_screen.show()


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
