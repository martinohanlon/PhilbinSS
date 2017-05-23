import itertools
from components import Power
from logicgates import Not, And, Or, Xor
import operator

def logic_gate_test(logic_gate, op):
    #how many inputs
    no_inputs = len(logic_gate.inputs)

    #create power switch for each input
    power = []
    for i in range(no_inputs):
        p = Power()
        p.connect(logic_gate.inputs[i])
        power.append(p)
    
    #loop through possible states
    results = []
    for state in get_binary_states(no_inputs):
        #set the power switches
        for i in range(no_inputs):
            power[i].value = state[i]

        #test the result
        result = op(*state)
        assert logic_gate.output.value == result

    return results

def get_binary_states(no_inputs):
    return list(itertools.product(*[(False, True)] * no_inputs))

def test_not():
    logic_gate_test(Not(), operator.__not__)
    
def test_and():
    logic_gate_test(And(), operator.__and__)
        
def test_or():
    logic_gate_test(Or(), operator.__or__)

def test_xor():
    logic_gate_test(Xor(), operator.__xor__)
    
def run_tests():
    test_not()
    test_or()
    test_and()
    test_xor()
    
    print("logicgates - all tests run")
    
run_tests()