import os
import numpy as np
import qiskit as qiskit
import qiskit_superstaq as qss
import matplotlib.pyplot as plt

token = "b62208c40e597889b171d9b14da25a798ea3a9d2ee5e5fcad4206c08dbd5988c"
os.environ["SUPERSTAQ_API_KEY"] = token

# Getting provider
provider = qss.SuperstaqProvider()

# Create circuit
theta = np.random.uniform(0, 4 * np.pi)
circuit1 = qiskit.QuantumCircuit(2)
circuit1.cx(0, 1)
circuit1.rz(theta, 1)
circuit1.cx(0, 1)
circuit1.measure_all()

# Draw circuit
circuit1.draw(output="mpl")
plt.show()

# Compile with qscout compile
compiler_output = provider.qscout_compile(circuit1)
compiler_output.circuit.draw("mpl")