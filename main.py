# main.py
import sys
from PyQt5.QtWidgets import QApplication
from start_window import StartWindow

def main():
    app = QApplication(sys.argv)
    win = StartWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
