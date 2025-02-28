from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PIL import Image
import os
import imghdr
from io import BytesIO

SUPPORTED_FORMATS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp']
CONVERSION_FORMATS = ['PNG', 'JPG', 'WEBP', 'GIF', 'BMP']

class ConversionScreen(QWidget):
    def __init__(self, go_back_callback=None):
        super().__init__()
        self.go_back_callback = go_back_callback
        self.setWindowTitle("Conversion Screen")
        self.setStyleSheet("background-color: #111; color: white;")

        # File attributes
        self.file_path: str = ""
        self.file_format: str = ""
        self.file_size: int = 0
        self.output_directory: str = ""

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(50, 50, 50, 50)

        # Header label
        self.header_label = QLabel("Kommverters")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.header_label.setStyleSheet(
            "font-size: 32px; font-weight: bold; color: #FF8800; background-color: transparent;"
        )
        self.layout.addWidget(self.header_label)

        # Wrapper container with styled layout
        self.wrapper_container = QWidget()
        self.wrapper_container.setStyleSheet(
            "background-color: #222; border-radius: 10px; padding: 10px;"
        )
        self.wrapper_layout = QVBoxLayout(self.wrapper_container)

        # File display layout (preview, file name, and close button in the same row)
        self.file_display_layout = QHBoxLayout()
        self.file_display_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.image_preview = QLabel()
        self.file_name_label = QLabel("")
        self.file_name_label.setStyleSheet("font-size: 16px; color: #FFFFFF;")

        self.file_display_layout.addWidget(self.image_preview)
        self.file_display_layout.addWidget(self.file_name_label)

        # Add a stretch so the close button will stay on the far right
        self.file_display_layout.addStretch()

        # Close (X) button
        self.close_button = QPushButton("✕")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("""
            QPushButton { 
                color: #FF8800;  
                font-size: 18px; 
                font-weight: bold; 
                background-color: #333; 
                border: 1px solid #FF8800;
                border-radius: 15px;
            }
            QPushButton:hover { 
                color: white;
                background-color: #FF8800;
            }
        """)
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_button.clicked.connect(self.go_back)

        self.file_display_layout.addWidget(self.close_button)

        # Finally, add this layout to the wrapper
        self.wrapper_layout.addLayout(self.file_display_layout)


        # Output options layout
        self.output_layout = QHBoxLayout()
        self.output_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Format selection
        self.format_layout = QVBoxLayout()
        self.format_label = QLabel("Format:")
        self.format_label.setStyleSheet("color: #3c83cf; font-size: 15px; margin-bottom: -14px; margin-left: -10px;")
        self.desired_format = QComboBox()
        self.desired_format.addItems(CONVERSION_FORMATS)
        self.desired_format.setStyleSheet(self._combo_box_style())
        self.format_layout.addWidget(self.format_label)
        self.format_layout.addWidget(self.desired_format)

        # Output name input
        self.output_name_layout = QVBoxLayout()
        self.output_name_label = QLabel("Output Name:")
        self.output_name_label.setStyleSheet("color: #3c83cf; font-size: 15px; margin-bottom: -14px; margin-left: -10px;")
        self.output_name = QLineEdit()
        self.output_name.setStyleSheet("background-color: #333; color: white;")
        self.output_name_layout.addWidget(self.output_name_label)
        self.output_name_layout.addWidget(self.output_name)

        # Size selection
        self.size_layout = QVBoxLayout()
        self.size_label = QLabel("Size:")
        self.size_label.setStyleSheet("color: #3c83cf; font-size: 15px; margin-bottom: -14px; margin-left: -10px;")
        self.size_combo = QComboBox()
        self.size_combo.addItems(["1", "0.8", "0.6", "0.4", "0.2"])
        self.size_combo.setStyleSheet(self._combo_box_style())
        self.size_layout.addWidget(self.size_label)
        self.size_layout.addWidget(self.size_combo)

        self.output_layout.addLayout(self.format_layout)
        self.output_layout.addLayout(self.output_name_layout)
        self.output_layout.addLayout(self.size_layout)
        self.wrapper_layout.addLayout(self.output_layout)

        self.layout.addWidget(self.wrapper_container)

        # Conversion controls layout
        self.convert_layout = QHBoxLayout()
        self.convert_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.convert_layout.setContentsMargins(0, 0, 0, 0)
        self.convert_layout.setSpacing(10)

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_file)
        self.convert_button.setStyleSheet("""
            QPushButton {
                background-color: #FF8800;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #FFA500;
            }
        """)

        # File size label that will display the estimated output file size
        self.file_size_label = QLabel("Estimated File Size: 0 KB")
        self.file_size_label.setStyleSheet("color: #FF8800; font-size: 15px; margin-right: 10px; background-color: transparent;")
        self.file_size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.file_source = QComboBox()
        self.file_source.addItems(["Same Folder", "Browse..."])
        self.file_source.currentIndexChanged.connect(self.update_output_path)
        self.file_source.setStyleSheet("""
            QComboBox {
                background-color: #FF8800;
                color: white;
                padding: 5px;
                border-radius: 5px;
                font-size: 16px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #555;
                border-left-style: solid;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
                border: none;
                background-color: transparent;
                color: white;
            }
            QComboBox::down-arrow {
                image: url(arrow-down.png);
                width: 20px;
                height: 20px;
                margin-right: 10px;
            }
        """)

        self.convert_layout.addWidget(self.convert_button, 2)
        self.convert_layout.addWidget(self.file_size_label, 1)
        self.convert_layout.addWidget(self.file_source, 1)
        self.layout.addLayout(self.convert_layout)

        # Update estimated file size when the size selection changes
        self.size_combo.currentIndexChanged.connect(self.update_estimated_file_size)

    def _combo_box_style(self) -> str:
        """Return the common style for combo boxes."""
        return """
            QComboBox {
                background-color: #333;
                color: white;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #555;
                border-left-style: solid;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
                border: none;
                background-color: #333;
                color: white;
            }
            QComboBox::down-arrow {
                image: url(arrow-down.png);
                width: 20px;
                height: 20px;
                margin-right: 10px;
            }
        """

    def set_file(self, file_path: str) -> None:
        """Set the file path and update UI elements accordingly."""
        self.file_path = file_path
        self.file_format = self.detect_file_format(file_path)
        file_name = os.path.basename(file_path)
        self.file_size = os.path.getsize(file_path)
        formatted_size = self.format_file_size(self.file_size)
        self.file_name_label.setText(f"{file_name}\n{formatted_size}")
        self.update_format_options()
        self.show_preview()
        self.update_output_name()
        self.update_estimated_file_size()

    def detect_file_format(self, file_path: str) -> str:
        """Detect file format using the file extension and imghdr."""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower().lstrip('.')
        if ext in SUPPORTED_FORMATS:
            detected = imghdr.what(file_path)
            return detected if detected else ext
        return ext

    def update_format_options(self) -> None:
        """Update the desired format options excluding the current file format."""
        self.desired_format.clear()
        current_format = 'jpg' if self.file_format in ['jpg', 'jpeg'] else self.file_format
        formats = [fmt.upper() for fmt in CONVERSION_FORMATS if fmt.lower() != current_format]
        self.desired_format.addItems(formats)
        self.update_output_name()

    def update_output_name(self) -> None:
        """Update the output name field based on selected options."""
        if not self.file_path:
            return
        file_name = os.path.splitext(os.path.basename(self.file_path))[0]
        target_format = self.desired_format.currentText().lower() if self.desired_format.currentText() else self.file_format
        directory = self.output_directory if self.output_directory else os.path.dirname(self.file_path)
        self.output_name.setText(os.path.join(directory, f"{file_name}.{target_format}"))

    def show_preview(self) -> None:
        """Display a preview of the image if supported."""
        if self.file_format in SUPPORTED_FORMATS:
            pixmap = QPixmap(self.file_path)
            pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_preview.setPixmap(pixmap)
        else:
            self.image_preview.clear()

    def format_file_size(self, size_bytes: int) -> str:
        """Return a human-readable file size."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        return f"{size_bytes / (1024 * 1024):.1f} MB"

    def update_estimated_file_size(self) -> None:
        """
        Estimate the output file size by resizing the image in memory with the
        selected scale factor and updating the file size label.
        """
        if not self.file_path:
            return
        try:
            scale = float(self.size_combo.currentText())
            img = Image.open(self.file_path)
            new_width = int(img.width * scale)
            new_height = int(img.height * scale)
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            buffer = BytesIO()
            target_format = self.desired_format.currentText() if self.desired_format.currentText() else self.file_format
            save_format = target_format.upper()
            resized_img.save(buffer, format=save_format)
            estimated_size = buffer.tell()
            formatted_size = self.format_file_size(estimated_size)
            self.file_size_label.setText(f"Estimated File Size: {formatted_size}")
        except Exception as e:
            self.file_size_label.setText("Estimated File Size: N/A")
            print("Error estimating file size:", e)

    def convert_file(self) -> None:
        """Perform the image file conversion with the selected scaling factor."""
        if not self.file_path:
            QMessageBox.warning(self, "No File", "Please select a file to convert.")
            return

        try:
            scale = float(self.size_combo.currentText())
            target_format = self.desired_format.currentText().lower()
            output_path = self.get_output_path(target_format)

            img = Image.open(self.file_path)
            new_width = int(img.width * scale)
            new_height = int(img.height * scale)
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)

            # Convert mode if needed for JPEG output
            if resized_img.mode == 'RGBA' and target_format in ['jpg', 'jpeg']:
                resized_img = resized_img.convert('RGB')

            resized_img.save(output_path)
            QMessageBox.information(self, "Success", f"Conversion successful:\n{output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Conversion failed: {str(e)}")

    def get_output_path(self, target_format: str) -> str:
        """
        Generate the output path based on the selected output directory,
        file name, and target format.
        """
        directory = self.output_directory if self.output_directory else os.path.dirname(self.file_path)
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        # If a custom output name is provided, use its directory and name
        custom_output = self.output_name.text().strip()
        if custom_output:
            directory = os.path.dirname(custom_output)
            base_name = os.path.splitext(os.path.basename(custom_output))[0]
        return os.path.join(directory, f"{base_name}.{target_format}")

    def update_output_path(self) -> None:
        """Update the output directory based on the file source selection."""
        if not self.file_path:
            return

        if self.file_source.currentText() == "Browse...":
            directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
            if directory:
                self.output_directory = directory
                self.update_output_name()
        else:
            self.output_directory = ""
            self.update_output_name()

    def go_back(self):
        if self.go_back_callback:
            self.go_back_callback()
        else:
            # Fallback: try to get the main window from the widget tree.
            main_window = self.window()
            if hasattr(main_window, 'drop_label'):
                main_window.setCentralWidget(main_window.drop_label)

