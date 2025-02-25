from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from drop_screen import DropLabel
from convertion_screen import ConvertionScreen
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kommverters")
        self.setMinimumSize(600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.drop_label = DropLabel(self.show_convertion_screen)
        self.layout.addWidget(self.drop_label)

        self.convertion_screen = ConvertionScreen()

    def show_convertion_screen(self, file_path):
        self.convertion_screen.set_file(file_path)
        self.setCentralWidget(self.convertion_screen)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()