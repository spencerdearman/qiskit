from qiskit import *
import matplotlib.pyplot as plt
from qiskit.visualization import plot_state_city, plot_histogram
from qiskit.visualization import plot_bloch_multivector, plot_state_hinton
from qiskit.visualization import plot_state_paulivec, plot_state_qsphere
 
# # Save an IBM Quantum account and set it as your default account.
# QiskitRuntimeService.save_account(channel="ibm_quantum", token="<TOKEN>", 
# set_as_default=True)

# Part I ---------------------------------------------------------------------
# Create a Quantum Circuit acting on a quantum register of three qubits
circ = QuantumCircuit(3)

# Add a H gate on qubit $q_{0}$, putting this qubit in superposition.
circ.h(0)
# Add a CX (CNOT) gate on control qubit $q_{0}$ and target qubit $q_{1}$, 
# putting the qubits in a Bell state.
circ.cx(0, 1)
# Add a CX (CNOT) gate on control qubit $q_{0}$ and target qubit $q_{2}$, 
# putting the qubits in a GHZ state.
circ.cx(0, 2)
circ.draw('mpl')

# Run the quantum circuit on a statevector simulator backend
backend = Aer.get_backend('statevector_simulator')

# Create a Quantum Program for execution
job = backend.run(circ)
result = job.result()

# Getting output
outputstate = result.get_statevector(circ, decimals=3)
print(outputstate)

# Real and imaginary components of the state density matrix 
plot_state_city(outputstate)

# Part II --------------------------------------------------------------------
# Quantum circuit to make a Bell state
bell = QuantumCircuit(2, 2)
bell.h(0)
bell.cx(0, 1)

# Measuring circuit
meas = QuantumCircuit(2, 2)
meas.measure([0,1], [0,1])

# Execute the quantum circuit
backend = BasicAer.get_backend('qasm_simulator') # the device to run on
circ = bell.compose(meas)
result = backend.run(transpile(circ, backend), shots=1000).result()
counts  = result.get_counts(circ)
print(counts)
plot_histogram(counts)

# Execute 2-qubit Bell state again
second_result = backend.run(transpile(circ, backend), shots=1000).result()
second_counts  = second_result.get_counts(circ)
# Plot results with legend
legend = ['First execution', 'Second execution']
plot_histogram([counts, second_counts], legend=legend)
# plt.show()

# Part III -------------------------------------------------------------------
# Different types of plots available 
# - plot_state_city(quantum_state)
# - plot_state_qsphere(quantum_state)
# - plot_state_paulivec(quantum_state)
# - plot_state_hinton(quantum_state)
# - plot_bloch_multivector(quantum_state)
# execute the quantum circuit

backend = BasicAer.get_backend('statevector_simulator') # the device to run on
result = backend.run(transpile(bell, backend)).result()
psi  = result.get_statevector(bell)
plot_bloch_multivector(psi)
plt.show()