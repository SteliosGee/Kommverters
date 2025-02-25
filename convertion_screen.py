from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QFileDialog, QComboBox, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QPixmap
import os


class ConvertionScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversion Screen")
        self.setStyleSheet("background-color: #111; color: white;")

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(50, 50, 50, 50)

        self.label = QLabel("Kommverters")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label.setStyleSheet("font-size: 32px; font-weight: bold; color: #FF8800; background-color: transparent;")

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
        self.desired_format.setStyleSheet("""
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
                                            """)
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
        self.size_combo.setStyleSheet("""
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
                                      """)
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

        self.convert_layout = QHBoxLayout()
        self.convert_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.convert_layout.setContentsMargins(0, 0, 0, 0)
        self.convert_layout.setSpacing(10)  # Adjust spacing

        self.convert_button = QPushButton("Convert")
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

        self.file_size_label = QLabel("File Size: 0 KB")
        self.file_size_label.setStyleSheet("color: #FF8800; font-size: 15px; margin-right: 10px; background-color: transparent;")
        self.file_size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center text

        self.file_source = QComboBox()
        self.file_source.addItems(["Local", "URL"])
        self.file_source.setStyleSheet("""
            QComboBox {
                background-color: #333;
                color: white;
                padding: 5px;
                border-radius: 5px;
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
                background-color: #333;
                color: white;
            }
            QComboBox::down-arrow {
                image: url(arrow-down.png);
                width: 20px;
                height: 20px;
                margin-right: 10px;
            }
        """)

        # Add widgets and set stretch factors
        self.convert_layout.addWidget(self.convert_button)
        self.convert_layout.addWidget(self.file_size_label)
        self.convert_layout.addWidget(self.file_source)

        self.convert_layout.setStretch(0, 2)  # Convert button takes more space
        self.convert_layout.setStretch(1, 1)  # File size label takes moderate space
        self.convert_layout.setStretch(2, 1)  # File source dropdown also gets space

        self.layout.addLayout(self.convert_layout)




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
