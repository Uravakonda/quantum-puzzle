from math import pi
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow,QListWidgetItem,QMessageBox,QTableWidgetItem
from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, state_fidelity
from puzzles import get_puzzles

class PuzzleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/puzzle_window.ui",self)

        self.sim = AerSimulator(method="statevector")
        self.circuitTableWidget.setRowCount(2)
        self.circuitTableWidget.setColumnCount(5)
        self.circuitTableWidget.clearContents()
        self.puzzles = get_puzzles()
        self.current_index = 0
        self.current = None
        self.gateListWidget.itemClicked.connect(self.add_gate_to_table)
        self.runButton.clicked.connect(self.evaluate_circuit)
        self.resetButton.clicked.connect(self.reset_circuit)
        self.hintButton.clicked.connect(self.show_hint)
        self.load_puzzle(self.current_index)

    def load_puzzle(self, index):
        self.current_index = index
        self.current = self.puzzles[index]
        self.questionLineEdit.setText(self.current["question"])
        self.reset_circuit()
        self.gateListWidget.clear()
        if self.current["qubits"] == 1:
            for g in ["H","Z","S","T", "RX(pi/2)","RZ(pi/4)"]:
                self.gateListWidget.addItem(QListWidgetItem(g))
        else:
            #this condition is for the two qubit questions
            for g in ["H0", "H1","CNOT","SWAP"]:
                self.gateListWidget.addItem(QListWidgetItem(g))

    def reset_circuit(self):
        self.circuitTableWidget.clearContents()
        self.circuitLineEdit.clear()
        self.resultTextEdit.clear()

    def add_gate_to_table(self, item):
        text = item.text()
        n = self.current["qubits"]
        placed = False
        for col in range(self.circuitTableWidget.columnCount()):
            if n == 1:
                if not self.circuitTableWidget.item(0,col):
                    self.circuitTableWidget.setItem(0,col,QTableWidgetItem(text))
                    placed = True
            else:
                if text in ("CNOT","SWAP"):
                    if not self.circuitTableWidget.item(0,col) and not self.circuitTableWidget.item(1,col):
                        self.circuitTableWidget.setItem(0, col,QTableWidgetItem(text))
                        self.circuitTableWidget.setItem(1,col, QTableWidgetItem(text))
                        placed = True
                else:
                    row = 0 if text.endswith("0") else 1
                    if not self.circuitTableWidget.item(row,col):
                        self.circuitTableWidget.setItem(row,col,QTableWidgetItem(text))
                        placed = True
            if placed:
                break
        #validation for if the table is full of gates
        if not placed:
            QMessageBox.warning(self, "Table Full", "No empty slot available.")
            return
        self._update_circuit_lineedit() #this will go to the methodto display teh circuit built by the user in a readable way

    def _update_circuit_lineedit(self):
        seq = []
        n = self.current["qubits"]
        cols = self.circuitTableWidget.columnCount()
        for col in range(cols):
            if n == 1:
                itm = self.circuitTableWidget.item(0,col)
                if itm:
                    seq.append(itm.text())
            else:
                i0 = self.circuitTableWidget.item(0, col)
                i1 = self.circuitTableWidget.item(1,col)
                if i0 and i1 and i0.text() == i1.text() and i0.text() in ("CNOT","SWAP"):
                    seq.append(i0.text())
                else:
                    if i0:
                        seq.append(f"{i0.text()}@0")
                    if i1:
                        seq.append(f"{i1.text()}@1")
        self.circuitLineEdit.setText("  |  ".join(seq))

    def build_qiskit_circuit(self):
        qc = self.current["solution"]().copy()
        qc.data.clear()
        n = self.current["qubits"]
        cols = self.circuitTableWidget.columnCount()
        for col in range(cols):
            name0 = (
                self.circuitTableWidget.item(0, col).text()
                if self.circuitTableWidget.item(0,col)
                else None
            )
            name1 = (self.circuitTableWidget.item(1,col).text()
                if n == 2 and self.circuitTableWidget.item(1,col)
                else None
            )
            #this is where gates used are applied
            if name0 in ("H","H0"):
                qc.h(0)
            if name0 == "Z":
                qc.z(0)
            if name0 == "S":
                qc.s(0)
            if name0 == "T":
                qc.t(0)
            if name0 == "RX(pi/2)":
                qc.rx(pi/2, 0)
            if name0 == "RZ(pi/4)":
                qc.rz(pi/4, 0)
            if name1 == "H1":
                qc.h(1)
            if name0 == "CNOT":
                qc.cx(0,1)
            if name0 == "SWAP":
                qc.swap(0,1)
        return qc

    def evaluate_circuit(self):
        qc = self.build_qiskit_circuit()
        tqc = transpile(qc, self.sim)
        tqc.save_statevector()
        job = self.sim.run(tqc)
        result = job.result().get_statevector(tqc)
        psi = Statevector(result)
        fid = state_fidelity(self.current["target_state"],psi) #this calculates the fidelity value for how the answer compares to teh solution
        self.resultTextEdit.append(f"Fidelity: {fid:.4f}")
        if fid > 0.99:
            QMessageBox.information(self,"Correct!", "Puzzle solved!")
            if self.current_index < len(self.puzzles) -1:
                self.load_puzzle(self.current_index +1)
            else:
                QMessageBox.information(self,"Done!","You've solved all puzzles.")

    def show_hint(self):
        #this method will be used for displaying the hint to visualise like its a circuit
        raw = self.current["solution"]().draw(output="text")
        hint = str(raw)
        QMessageBox.information(self,"Hint (full solution)",hint)
