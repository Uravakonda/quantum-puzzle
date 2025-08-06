import sys
from PyQt5.QtWidgets import QApplication
from start_window import StartWindow

def main():
    app = QApplication(sys.argv)
    #This stylesheet below is for the QMessageBox formatting so it is consistent with the rest of the GUIs
    app.setStyleSheet("""
        QMessageBox {
            background-color: white;
            color: black;
            font-family: Futura;
            font-size: 14px;
        }
        QMessageBox QLabel {
            color: black;
        }
        QMessageBox QPushButton {
            background-color: rgb(140,200,255);
            color: white;
            border-radius: 10px;
            padding: 5px 10px;
            border: none;
        }
        QMessageBox QPushButton:hover {
            background-color: rgb(155,186,255);
        }""")

    window = StartWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
