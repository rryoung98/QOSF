from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister 

from draper_adder import draper_adder

list_of_int = [5,7,8,9,1]
output = 16
"{0:b}".format(list_of_int[0])

def create_quantum_registers(list_of_int:list=[5,7,8,9,1]) -> dict:
    largest_num = max(list_of_int)
    quantum_circuit_dict = {}
    for int in list_of_int:
        q1 = QuantumRegister(largest_num, name=f"q_{int}")
        qc = QuantumCircuit(q1)
        binary_rep = "{0:b}".format(int)
        for i,binary in enumerate(binary_rep):
            if binary == "1":
                print(i)
                qc.x(q1[i])
        # make dictionary
        quantum_circuit_dict[int] = qc
    return quantum_circuit_dict

the_dict = create_quantum_registers(list_of_int)
print(the_dict[9])