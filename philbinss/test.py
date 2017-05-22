import itertools
from components import Power
from logicgates import And

def get_logic_gate_results(logic_gate):
    no_inputs = len(logic_gate.inputs)
    #create power for each input
    power = []
    for i in range(no_inputs):
        p = Power()
        p.connect(logic_gate.inputs[i])
        power.append(p)
    
    #loop through possible states
    results = []
    for state in get_states(no_inputs):
        for i in range(no_inputs):
            power[i].value = state[i]
        results.append([state,logic_gate.output.value])
        
    return results

def get_states(no_inputs):
    return list(itertools.product(*[(False, True)] * no_inputs))

def run_tests():
    #test And
    results = get_logic_gate_results(And())
    