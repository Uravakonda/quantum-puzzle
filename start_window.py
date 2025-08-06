from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from puzzle_window import PuzzleWindow
from bloch_window import BlochWindow

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/start_window.ui",self)

        self.playbtn.clicked.connect(self.open_puzzle)
        self.exitbtn.clicked.connect(self.close)
        self.blochbtn.clicked.connect(self.open_sandbox)

    def open_puzzle(self):
        self.puzzle_win = PuzzleWindow()
        self.puzzle_win.show()

    def open_sandbox(self):
        self.sandbox_win = BlochWindow()
        self.sandbox_win.show()
