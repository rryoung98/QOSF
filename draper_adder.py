from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister ,Aer, assemble
from numpy import pi
def qft_rotations(circuit:QuantumCircuit, n:int) -> QuantumCircuit:
    """QFT without swap on the first n qubits in circuit
    Args:
        circuit (QuantumCircuit): The circuit to apply the QFT to
        n (int): Number of qubits to apply the QFT to

    Returns:
        None
    
    Credit: https://qiskit.org/textbook/ch-algorithms/quantum-fourier-transform.html
    """    
    if n == 0: # Exit function if circuit is empty
        return circuit
    n -= 1 # Indexes start from 0
    circuit.h(n) # Apply the H-gate to the most significant qubit
    for qubit in range(n):
        # For each less significant qubit, we need to do a
        # smaller-angled controlled rotation: 
        circuit.cp(pi/2**(n-qubit), qubit, n)
    qft_rotations(circuit, n)

# apply inverse qft

def inverse_qft(circuit, n):
    """Does the inverse QFT on the first n qubits in circuit"""
    # First we create a QFT circuit of the correct size:
    circ = QuantumCircuit(n)
    qft_rotations(circ, n)
    # Then we take the inverse of this circuit
    invqft_circ = circ.inverse()
    # And add it to the first n qubits in our existing circuit
    circuit.append(invqft_circ, circuit.qubits[:n])
    return circuit.decompose() # .decompose() allows us to see the individual gates


def draper_adder(num_qubits : int) -> QuantumCircuit:
    """Creates a quantum circuit that adds two integers via the Draper method.
        https://arxiv.org/pdf/quant-ph/0008033.pdf
    Args:
        num_qubits (int): The number of qubits to use in the circuit.

    Returns:
        QuantumCircuit: The quantum circuit with the addition circuit.
    """    
    q1 = QuantumRegister(num_qubits+1) # add one for carry
    q2 = QuantumRegister(num_qubits)
    c1 = ClassicalRegister(num_qubits+1)
    qc = QuantumCircuit(q1, q2, c1)
    qc.x([q1[2], q2[2]])
    qft_rotations(qc, num_qubits+1)

    # # Apply controlled phase shift to the target qubit
    register_len = len(q2)
    for qubit in range(register_len):
        for idx in range(register_len-qubit):
            qc.cp(pi/2**(idx), q2[qubit], q1[qubit+idx])

    # Apply controlled phase shift for carry
    for idx in range(register_len):
        qc.cp(2*pi/2**(idx+2), q2[register_len-idx-1], q1[register_len])
    # Apply inverse qft
    inverse_qft(qc, num_qubits+1)
    # Apply measurement
    qc.measure(q1, c1)
    qc = qc.decompose()
    aer_sim = Aer.get_backend('aer_simulator')
    qobj = assemble(qc, shots=4096)
    job = aer_sim.run(qobj)
    print(job)
    hist = job.result().get_counts()
    print(hist)
    return qc

draper_adder(3)