# answers_window.py
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from puzzles import get_puzzles

class AnswersWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/answers_window.ui", self)
        self.puzzles = get_puzzles()
        self.load_answers()

    def load_answers(self):
        self.answersTableWidget.setRowCount(len(self.puzzles))
        for i, p in enumerate(self.puzzles):
            self.answersTableWidget.setItem(i, 0,
                QTableWidgetItem(p["name"]))
            sol_txt = str(p["solution"]().draw(output="text"))
            self.answersTableWidget.setItem(i, 1,
                QTableWidgetItem(sol_txt))
        self.answersTableWidget.resizeColumnsToContents()
