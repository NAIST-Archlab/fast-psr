import qiskit
import time
import numpy as np
from qiskit_aer import Aer
import ansatz
for i in range(1, 3):
    timess = []
    for num_qubits in range(3, 6):
        function_name = f'quanvolutional{i}'
        times = []
        for t in range(0, 10):
            start = time.time()
            qc = qiskit.QuantumCircuit(num_qubits) 
            
            qc = getattr(ansatz, function_name)(qc)
            qc.save_statevector()
            simulator = Aer.get_backend('aer_simulator_statevector', device = 'GPU')
            qc = qiskit.transpile(qc, backend = simulator)
            result = simulator.run(qc).result()
            statevector = result.get_statevector(qc)
            end = time.time()
            times.append(end-start)
        timess.append(np.mean(times))
        print(np.mean(times))
        np.savetxt(f'result/quanv_gpu30/quanv{i}.txt', timess)