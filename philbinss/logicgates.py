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

if __name__ == "__main__":
    
    x = Xor()
    i1 = Power()
    i2 = Power()
    #connect the power to the xor gates inputs
    i1.connect(x.input_a)
    i2.connect(x.input_b)
    print(x)
    i1.on()
    i2.off()
    print(x)
    i1.off()
    i2.on()
    print(x)
    i1.on()
    i2.on()
    print(x)
    i1.off()
    i2.off()
    print(x)

    #print("and1 " +str(x.a1))
    #print("not  " + str(x.n))
    #print("or   " + str(x.o))
    #print("or.t1 " + str(x.o.t1))
    #print("or.t2 " + str(x.o.t2))
    #print("and2 " + str(x.a2))
    #print("and2.t1 " + str(x.a2.t1))
    #print("and2.t2 " + str(x.a2.t2))
    

if __name__ == "__main__not":
    n = Not()
    i = Power()
    #connect the power to the not gates input
    i.connect(n.input)
    print(n)
    i.on()
    print(n)
    i.off()
    print(n)


if __name__ == "__main__and":
    a = And()
    i1 = Power()
    i2 = Power()
    #connect the power to the and gates inputs
    i1.connect(a.input_a)
    i2.connect(a.input_b)
    print(a)
    i1.on()
    print(a)
    i2.on()
    print(a)
    i2.off()
    print(a)
    i1.off()
    print(a)
    
if __name__ == "__main__or":
    o = Or()
    i1 = Power()
    i2 = Power()
    #connect the power to the or gates inputs
    i1.connect(o.input_a)
    i2.connect(o.input_b)
    i1.on()
    i2.off()
    print(o)
    i1.off()
    i2.on()
    print(o)
    i1.on()
    i2.on()
    print(o)
    i1.off()
    i2.off()
    print(o)
    

if __name__ == "__main__not_or":
    o = Or()
    n1 = Not()
    n2 = Not()
    i1 = Power()
    i2 = Power()
    #connect the power to the or gates inputs
    i1.connect(n1.input)
    i2.connect(n2.input)
    n1.output.connect(o.input_a)
    n2.output.connect(o.input_b)
    print(n1)
    print(n2)
    print(o)
    i1.on()
    i2.off()
    print(n1)
    print(n2)
    print(o)
    i1.off()
    i2.on()
    print(n1)
    print(n2)
    print(o)
    i1.on()
    i2.on()
    print(n1)
    print(n2)
    print(o)
    
