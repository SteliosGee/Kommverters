from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from drop_screen import DropLabel
from convertion_screen import ConversionScreen
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kommverters")
        self.setMinimumSize(600, 400)

        # Create the initial drop screen
        self.drop_label = DropLabel(self.show_convertion_screen)
        
        # Set the initial central widget
        self.setCentralWidget(self.drop_label)
        
    def show_convertion_screen(self, file_path):
        # Create a new conversion screen instance each time
        self.convertion_screen = ConversionScreen(self.show_drop_screen)
        self.convertion_screen.set_file(file_path)
        self.setCentralWidget(self.convertion_screen)

    def show_drop_screen(self):
        """Create a new drop label and set it as central widget"""
        self.drop_label = DropLabel(self.show_convertion_screen)
        self.setCentralWidget(self.drop_label)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()