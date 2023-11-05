from qiskit import *
from qiskit.extensions import Initialize
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
from numpy import append, sqrt
from numpy.random import random
"""
Tutorial From: https://www.qmunity.tech/tutorials/quantum-teleportation
Goal: Learning more about quantum entanglement and quantum circuitry.
"""

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
    # Putting qubit into a state |+⟩ and |-⟩ using the Hadamard gate 'h'
    qc.h(a) 
    # Controlled-not with a as the control and b as the target
    qc.cx(a,b)

entangle_bell_pair(teleportation_circuit, 1, 2)
# teleportation_circuit.draw(output='mpl')

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
# teleportation_circuit.draw(output='mpl')

# Measure States of Qubits ---------------------------------------------------
"""
Measuring both qubit 1 and |𝜓⟩, and storing this result into the two classical 
bits that I created earlier. Then going to send those two btis to qubit 2 in
order to not violate the no-cloning theorem.

No Cloning Theorem: It is impossible to create an identical copy of an arbitrary
unknown quantum state. There cannot be a physcial process that produces a copy
of a quantum state.
"""

def measure_classical_send(qc, a, b):
    qc.barrier()
    qc.measure(a, 0)
    qc.measure(b, 1)

measure_classical_send(teleportation_circuit, 0, 1)
# teleportation_circuit.draw(output='mpl')

# Decoding From Qubit 2 ------------------------------------------------------
"""
Based on the two classical bits passed in, the quantum gates applied will be 
different:

Bits:
    - 00 ->> Identity
    - 01 ->> Apply X Gate
    - 10 ->> Apply Z Gate
    - 11 ->> Apply ZX Gate
"""

def apply_gates(qc, qubit, cr1, cr2):
    qc.z(qubit).c_if(cr1, 1) # If cr1 is 1, apply the Z gate
    qc.x(qubit).c_if(cr2, 1) # If cr2 is 1 apply X gate, look at table above

teleportation_circuit.barrier() # Using barrier to separate steps
apply_gates(teleportation_circuit, 2, cr1, cr2)
# teleportation_circuit.draw(output='mpl')

# Using Quantum Simulator to Test --------------------------------------------
"""
Now I am going to initialize the conversion qubit |𝜓⟩ to a random state. This 
will be sued in order to initialize a gate on qubit 0. I will do this using a 
random state function.
"""
def random_state(nqubits):
    """Creates a random nqubit state vector"""
    real_parts = []
    im_parts = []
    for _ in range(2 ** nqubits):
        real_parts = append(real_parts, (random() * 2) - 1)
        im_parts = append(im_parts, (random() * 2) - 1)
    # Combine into list of complex numbers:
    amps = real_parts + 1j * im_parts
    # Normalise
    magnitude_squared = 0
    for a in amps:
        magnitude_squared += abs(a) ** 2
    amps /= sqrt(magnitude_squared)
    return amps

# specify a random state
psi = random_state(1)
# Defining Initialization gate to create |𝜓⟩ from |0⟩
init_gate = Initialize(psi)

# Testing Quantum Teleportation ----------------------------------------------
"""
Now I am going to test all of the functions and see if the teleportation
protocol works.
"""
qr = QuantumRegister(3)   
cr1 = ClassicalRegister(1) 
cr2 = ClassicalRegister(1)
qc = QuantumCircuit(qr, cr1, cr2)

# Initialize qubit 0
qc.append(init_gate, [0])
qc.barrier()

# teleportation protocol
entangle_bell_pair(qc, 1, 2)
qc.barrier()

# Send q1 to psi and qubit 2 to 0
state_qubits(qc, 0, 1)

# sending from 0 to 1
measure_classical_send(qc, 0, 1)

# decoding the qubits
apply_gates(qc, 2, cr1, cr2)

qc.draw(output='mpl')

# Execute on Backend ---------------------------------------------------------
"""
Actual execution.
"""
backend = BasicAer.get_backend('statevector_simulator')
out_vector = execute(qc, backend).result().get_statevector()
plot_bloch_multivector(out_vector)
"""
Quantum teleportation is used to send qubits between two different parties. 

    qubit 0 |0⟩     qubit 1 |0⟩     qubit 2 |0⟩

On a real quantum computer, we would not be able to use the state-vector, 
so to check teleportation circuit is working, we need to do things slightly 
differently. You will remember that we used Initialize to turn our |0⟩ 
qubit into the state |𝜓⟩.

All quantum gates are reversible, which means that we can find the inverse of 
the initialize function.
"""
# Initialize inverse
inverse_init_gate = init_gate.gates_to_uncompute()
qc.append(inverse_init_gate, [2])
qc.draw(output='mpl')

# Add a new classical register to see the result
cr_result = ClassicalRegister(1)
qc.add_register(cr_result)
qc.measure(2, 2)
qc.draw(output='mpl')

# Plotting the histogram of the results
backend = BasicAer.get_backend('qasm_simulator')
counts = execute(qc, backend, shots = 1024).result().get_counts()
plot_histogram(counts)
plt.show()