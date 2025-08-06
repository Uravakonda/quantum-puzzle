from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem
from PyQt5.QtGui import QPixmap
from qiskit import QuantumCircuit
from qiskit.visualization import plot_bloch_vector
from qiskit.quantum_info import Statevector
import numpy as np
import matplotlib.pyplot as plt
import os

class BlochWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/bloch_window.ui",self)

        self.qc = QuantumCircuit(1)
        self.update_bloch()
        for i in ["H", "X","Z", "S", "T","RX(pi/2)","RZ(pi/4)"]:
            self.gateListWidget.addItem(QListWidgetItem(i))
        self.applybtn.clicked.connect(self.apply_gate)
        self.resetbtn.clicked.connect(self.reset_circuit)

    def apply_gate(self):
        selected = self.gateListWidget.currentItem()
        if not selected:
            return

        gate = selected.text()
        if gate == "H":
            self.qc.h(0)
        elif gate == "X":
            self.qc.x(0)
        elif gate =="Z":
            self.qc.z(0)
        elif gate == "S":
            self.qc.s(0)
        elif gate =="T":
            self.qc.t(0)
        elif gate == "RX(pi/2)":
            self.qc.rx(np.pi / 2,0)
        elif gate == "RZ(pi/4)":
            self.qc.rz(np.pi / 4,0)
        self.update_bloch()

    def reset_circuit(self):
        self.qc = QuantumCircuit(1)
        self.update_bloch()

    def update_bloch(self):
        state = Statevector.from_instruction(self.qc)
        bloch_vector = self.manual_bloch_vector(state.data)
        bloch = plot_bloch_vector(bloch_vector)
        path = "bloch.png"
        bloch.savefig(path)
        bloch.clf()
        pixmap = QPixmap(path)
        self.blochImageLabel.setPixmap(pixmap)
        os.remove(path)

    #the method below is calculating teh bloch sphere state vector given the state.

    def manual_bloch_vector(self,state):
        state = state /np.linalg.norm(state)
        a, b = state[0],state[1]
        # code belw will map quantum state to 3D unit vector on sphere.
        x = 2 * (a.conjugate()* b).real
        y = 2 * (a.conjugate() *b).imag
        z = abs(a)**2 - abs(b)**2
        return np.array([x,y,z])
