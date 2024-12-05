from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    janela = MainWindow()
    janela.show()
    app.exec_()
