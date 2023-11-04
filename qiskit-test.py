import qiskit
from qiskit.test.reference_circuits import ReferenceCircuits
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
 
# # Save an IBM Quantum account and set it as your default account.
# QiskitRuntimeService.save_account(channel="ibm_quantum", token="6ab51482612c0c9f8e09ec7430f42a53681f6260f9909f31577e9cc1154316d0c182f336fe1499da352e6d910d16cf427d57fcbe0a3fbb225d373a713cd1b242", set_as_default=True)

# Load saved credentials
service = QiskitRuntimeService()

 # You'll need to specify the credentials when initializing QiskitRuntimeService, if they were not previously saved.
service = QiskitRuntimeService()
backend = service.backend("ibmq_qasm_simulator")
job = Sampler(backend).run(ReferenceCircuits.bell())
print(f"job id: {job.job_id()}")
result = job.result()
print(result)