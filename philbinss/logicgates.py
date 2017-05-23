from components import Transistor, Power, Join, Split

class LogicGate(object):
    def __init__(self, inputs, output):
        self._inputs = inputs
        self._output = output
        
    @property
    def output(self):
        return self._output

    @property
    def inputs(self):
        return self._inputs

    def __repr__(self):
        return "{},{}".format(self.inputs, self.output)

    def __str__(self):
        return "inputs = {}, output = {}".format(self.inputs, self.output)


class OneInputLogicGate(LogicGate):
    def __init__(self, theinput, output):
        inputs = [theinput]
        super(OneInputLogicGate, self).__init__(inputs, output)

    @property
    def input(self):
        return self._inputs[0]

class TwoInputLogicGate(LogicGate):
    def __init__(self, input_a, input_b, output):
        inputs = [input_a, input_b]
        super(TwoInputLogicGate, self).__init__(inputs, output)

    @property
    def input_a(self):
        return self._inputs[0]

    @property
    def input_b(self):
        return self._inputs[1]

class Not(OneInputLogicGate):
    def __init__(self):
        t = Transistor()

        theinput = t.base
        output = t.collector_output

        super(Not, self).__init__(theinput, output)

    def __str__(self):
        return "Not: input = {}, output = {}".format(self.input, self.output)
        
class And(TwoInputLogicGate):
    def __init__(self):
        t1 = Transistor()
        t2 = Transistor(connect_to_power = False)
        
        input_a = t1.base
        input_b = t2.base
        
        t1.emitter.connect(t2.collector)
        
        output = t2.emitter

        super(And, self).__init__(input_a, input_b, output)

    def __str__(self):
        return "And: input_a = {}, input_b = {}, output = {}".format(self.input_a, self.input_b, self.output)

class Or(TwoInputLogicGate):
    def __init__(self):
        t1 = Transistor()
        t2 = Transistor()

        input_a = t1.base
        input_b = t2.base

        #join the 2 transmitter emitters
        join = Join(t1.emitter, t2.emitter)
        
        output = join.output
        
        super(Or, self).__init__(input_a, input_b, output)

    def __str__(self):
        return "Or: input_a = {}, input_b = {}, output = {}".format(self.input_a, self.input_b, self.output)

class Xor(TwoInputLogicGate):
    def __init__(self):
        #create gates
        a1 = And()
        o = Or()
        n = Not()
        a2 = And()

        #split input a and b to go to the and1 and or gate 
        input_a = Split(a1.input_a, o.input_a).input
        input_b = Split(a1.input_b, o.input_b).input

        #output of and2 to not
        a1.output.connect(n.input)
        
        #output of not to and2
        n.output.connect(a2.input_a)
        
        #output of or to and2
        o.output.connect(a2.input_b)
        
        #output is the result of and2
        output = a2.output

        super(Xor, self).__init__(input_a, input_b, output)

    def __str__(self):
        return "Xor: input_a = {}, input_b = {}, output = {}".format(self.input_a, self.input_b, self.output)

