import qiskit
import time
import numpy as np
from qiskit_aer import Aer
import ansatz
import pandas as pd

def quanv(num_qubits, function_name):
    qc = qiskit.QuantumCircuit(num_qubits) 
    qc = getattr(ansatz, function_name)(qc)
    qc.save_statevector()
    simulator = Aer.get_backend('aer_simulator_statevector', device = 'GPU')
    qc = qiskit.transpile(qc, backend = simulator)
    result = simulator.run(qc).result()
    statevector = result.get_statevector(qc)
    return

for i in range(1, 10):
    quanv(10, 'quanvolutional1')  # Warm up the GPU
for num_qubits in range(29, 31):
    for i in range(1, 20):
        
        function_name = f'quanvolutional{i}'
        times = []
        for t in range(0, 10):
            start = time.time()
            quanv(num_qubits, function_name)
            end = time.time()
            times.append(end-start)
        record = {'num_qubits': num_qubits, 'quanvolutional': i, 'time': np.mean(times)}
        if 'results_df' not in locals():
            results_df = pd.DataFrame(columns=record.keys())
        results_df = pd.concat([results_df, pd.DataFrame([record])], ignore_index=True)
        results_df.to_csv(f'result/quanv_gpu_only30.csv', index=False)
        print(f'num_qubits: {num_qubits}, quanvolutional{i}, time: ', np.mean(times))
