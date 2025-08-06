# start_window.py
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from puzzle_window import PuzzleWindow
from answers_window import AnswersWindow

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/start_window.ui", self)

        # Connect buttons
        self.playButton.clicked.connect(self.open_puzzle)
        self.answersButton.clicked.connect(self.open_answers)
        self.exitButton.clicked.connect(self.close)

    def open_puzzle(self):
        self.puzzle_win = PuzzleWindow()
        self.puzzle_win.show()

    def open_answers(self):
        self.answer_win = AnswersWindow()
        self.answer_win.show()
