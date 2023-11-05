import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, BasicAer, IBMQ
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit import *
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram


# Setup ----------------------------------------------------------------------

# Make quantum register
qr = QuantumRegister(3)    
# Make classic registers 1 and 2
cr1 = ClassicalRegister(1)
cr2 = ClassicalRegister(1)
# Initializing circuit
teleportation_circuit = QuantumCircuit(qr, cr1, cr2)

# Creating entangled pair ----------------------------------------------------
"""
In order to make the entangled pair, I need to create a Bell pair. To create the
bell pair, I have to transfer one to the X-basis (|+⟩ and |-⟩). In order to do 
so, I need to use a Hadamard gate.

Hadamard gate: A logic gate that turns a state of |0⟩ or |1⟩ to the 
superposition version of |0⟩ or |1⟩. It converts the qubit from a custering 
state into a uniform superposed state. 

Qiskit uses a Hadamard gate as its basis. I also need to add a controlled not 
gate onto the other qubit controlled by the one in the X-basis.

CNOT Gate: A binary gate that is applied on two qubits that is the way used to
create an entangled pair.
"""

def entangle_bell_pair(qc, a, b):
    # Putting qubit into a state |+⟩ and |-⟩ using the hadamard gate 'h'
    qc.h(a) 
    # Controlled-not with a as the control and b as the target
    qc.cx(a,b)

entangle_bell_pair(teleportation_circuit, 1, 2)
teleportation_circuit.draw(output='mpl')

# Applying Quantum Gates -----------------------------------------------------
"""
Now I have to add a CNOT gate to qubit 1, which will be controlled by the third
qubit |𝜓⟩, or the qubit that is going to allow the entanglement to work. I am
now going to add a Hadamard gate to |𝜓⟩.
"""
def state_qubits(qc, psi, a):
    qc.cx(psi, a) # psi is going to represent the state of qubit 0
    qc.h(psi) # adding a Hadamard gate to psi

teleportation_circuit.barrier()
state_qubits(teleportation_circuit, 0, 1)
teleportation_circuit.draw(output='mpl')
plt.show()

# Measure States of Qubits ---------------------------------------------------
"""
"""