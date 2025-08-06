# puzzles.py

from math import sqrt, pi
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def get_puzzles():
    puzzles = []

    # 1. Plus State
    def plus_solution():
        qc = QuantumCircuit(1)
        qc.h(0)
        return qc

    puzzles.append({
        "name": "Plus State",
        "qubits": 1,
        "initial_state": [1, 0],
        "target_state": Statevector([1/sqrt(2), 1/sqrt(2)]),
        "solution": plus_solution,
        "question": "Transform |0⟩ into the |+⟩ = (|0⟩ + |1⟩)/√2 superposition using available single-qubit gates."
    })

    # 2. Minus State
    def minus_solution():
        qc = QuantumCircuit(1)
        qc.h(0)
        qc.z(0)
        return qc

    puzzles.append({
        "name": "Minus State",
        "qubits": 1,
        "initial_state": [1, 0],
        "target_state": Statevector([1/sqrt(2), -1/sqrt(2)]),
        "solution": minus_solution,
        "question": "Transform |0⟩ into the |–⟩ = (|0⟩ – |1⟩)/√2 superposition."
    })

    # 3. Phase π/4 State
    def phase_solution():
        qc = QuantumCircuit(1)
        qc.h(0)
        qc.rz(pi/4, 0)
        return qc

    puzzles.append({
        "name": "Phase π/4 State",
        "qubits": 1,
        "initial_state": [1, 0],
        "target_state": Statevector([
            1/sqrt(2),
            (1/sqrt(2)) * complex(sqrt(2)/2, sqrt(2)/2)
        ]),
        "solution": phase_solution,
        "question": "Prepare the state (|0⟩ + e^{iπ/4}|1⟩)/√2 from |0⟩."
    })

    # 4. Bell State
    def bell_solution():
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        return qc

    puzzles.append({
        "name": "Bell State",
        "qubits": 2,
        "initial_state": [1, 0, 0, 0],
        "target_state": Statevector([1/sqrt(2), 0, 0, 1/sqrt(2)]),
        "solution": bell_solution,
        "question": "Entangle two qubits starting from |00⟩ to create the Bell state (|00⟩ + |11⟩)/√2."
    })

    return puzzles
