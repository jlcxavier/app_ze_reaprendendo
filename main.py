from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    app = QApplication([])
    janela = MainWindow()
    janela.show()
    app.exec_()
