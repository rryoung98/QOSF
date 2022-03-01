"""Quantum circuit that adds two integers via the Draper method.
"""
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from numpy import pi



def qft_rotations(circuit: QuantumCircuit, num_qubits: int) -> QuantumCircuit:
    """QFT without swap on the first n qubits in circuit
    Args:
        circuit (QuantumCircuit): The circuit to apply the QFT to
        n (int): Number of qubits to apply the QFT to

    Returns:
        None

    Credit: https://qiskit.org/textbook/ch-algorithms/quantum-fourier-transform.html
    """
    if num_qubits == 0: # Exit function if circuit is empty
        return circuit
    num_qubits -= 1 # Indexes start from 0
    circuit.h(num_qubits) # Apply the H-gate to the most significant qubit
    for qubit in range(num_qubits):
        # For each less significant qubit, we need to do a
        # smaller-angled controlled rotation:
        circuit.cp(pi/2**(num_qubits-qubit), qubit, num_qubits)
    qft_rotations(circuit, num_qubits)
    return None

def inverse_qft(circuit: QuantumCircuit, num_qubits: int) -> QuantumCircuit:
    """Does the inverse QFT on the first n qubits in circuit"""
    # First we create a QFT circuit of the correct size:
    circ = QuantumCircuit(num_qubits)
    qft_rotations(circ, num_qubits)
    # Then we take the inverse of this circuit
    invqft_circ = circ.inverse()
    # And add it to the first n qubits in our existing circuit
    circuit.append(invqft_circ, circuit.qubits[:num_qubits])
    return circuit.decompose() # .decompose() allows us to see the individual gates

#pylint: disable=line-too-long
def embed_integers(circuit: QuantumCircuit, register: QuantumRegister, binary_rep: str) -> QuantumCircuit:
    """Embeds an integer into a circuit

    Args:
        circuit (QuantumCircuit): The circuit to embed the integer into.
        register (QuantumRegister): The register to embed the integer into.
        integer (int): The integer to embed.

    Returns:
        QuantumCircuit: The circuit with the integer embedded.
    """

    for i, binary in enumerate(binary_rep):
        if binary == "1":
            circuit.x(register[i])
    return circuit


def draper_adder(int_1: int = 7, int_2: int = 5) -> QuantumCircuit:
    """Creates a quantum circuit that adds two integers via the Draper method.
        https://arxiv.org/pdf/quant-ph/0008033.pdf
    Args:
        int_1 (int): The first integer to add.
        int_2 (int): The second integer to add.

    Returns:
        QuantumCircuit: The quantum circuit with the addition circuit.
    """
    if (int_1 < 0) or (int_2 < 0):
        raise ValueError("Draper adder only works for positive integers")
    binary_rep_1 = "{0:b}".format(int_1)
    binary_rep_2 = "{0:b}".format(int_2)
    num_qubits = max(len(binary_rep_2), len(binary_rep_1))
    q_1 = QuantumRegister(num_qubits+1) # add one for carry
    q_2 = QuantumRegister(num_qubits)
    c_1 = ClassicalRegister(num_qubits+1)
    circ = QuantumCircuit(q_1, q_2, c_1)

    # Embed int_1 and int_2
    embed_integers(circ, q_1, binary_rep_1)
    embed_integers(circ, q_2, binary_rep_2)

    qft_rotations(circ, num_qubits+1)

    # # Apply controlled phase shift to the target qubit
    register_len = len(q_2)
    for qubit in range(register_len):
        for idx in range(register_len-qubit):
            circ.cp(pi/2**(idx), q_2[qubit], q_1[qubit+idx])

    # Apply controlled phase shift for carry
    for idx in range(register_len):
        circ.cp(2*pi/2**(idx+2), q_2[register_len-idx-1], q_1[register_len])
    # Apply inverse qft
    inverse_qft(circ, num_qubits+1)
    # Apply measurement
    circ.measure(q_1, c_1)
    circ = circ.decompose()
    return circ
