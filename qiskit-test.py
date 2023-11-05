from qiskit import *
import matplotlib.pyplot as plt
from qiskit.visualization import plot_state_city
from qiskit.tools.monitor import job_monitor
from qiskit.tools.visualization import plot_histogram
from qiskit.test.reference_circuits import ReferenceCircuits
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
 
# # Save an IBM Quantum account and set it as your default account.
# QiskitRuntimeService.save_account(channel="ibm_quantum", token="6ab51482612c0c9f8e09ec7430f42a53681f6260f9909f31577e9cc1154316d0c182f336fe1499da352e6d910d16cf427d57fcbe0a3fbb225d373a713cd1b242", set_as_default=True)


# # Part I

# # Load saved credentials
# service = QiskitRuntimeService()

# # build 2 qubit quantum register
# qr = QuantumRegister(2)

# # building 2 classical bit classical register
# cr = ClassicalRegister(2)

# # quantum circuit
# circuit = QuantumCircuit(qr, cr)

# # hadamard gate 
# circuit.h(qr[0])

# # controlled X gate
# circuit.cx(qr[0], qr[1])

# # measure qubits and put into classical register
# circuit.measure(qr, cr)

# # simulate quantum circuit -- using air
# simulator = Aer.get_backend('qasm_simulator')
# result = execute(circuit, backend = simulator).result()

# plotting results from simulator 
# plot_histogram(result.get_counts(circuit))
# circuit.draw(output='mpl') 
# plt.show()


# Part II

# Create a Quantum Circuit acting on a quantum register of three qubits
circ = QuantumCircuit(3)

# Add a H gate on qubit $q_{0}$, putting this qubit in superposition.
circ.h(0)
# Add a CX (CNOT) gate on control qubit $q_{0}$ and target qubit $q_{1}$, putting
# the qubits in a Bell state.
circ.cx(0, 1)
# Add a CX (CNOT) gate on control qubit $q_{0}$ and target qubit $q_{2}$, putting
# the qubits in a GHZ state.
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

plot_state_city(outputstate)
plt.show()

# # You'll need to specify the credentials when initializing QiskitRuntimeService, if they were not previously saved.
# backend = service.backend("ibmq_qasm_simulator")
# job = Sampler(backend).run(circuit)
# print(f"job id: {job.job_id()}")
# job_monitor(job)
# q_result = job.result()
# # counts = q_result.data().get('counts')
# plot_histogram(q_result.quasi_dists[0])
# # print(dir(q_result))

