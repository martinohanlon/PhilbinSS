from components import Base, Transistor, Power, Join, Split
from mixins import OneInputMixin, TwoInputMixin, OneOutputMixin

class Not(Base, OneInputMixin, OneOutputMixin):
    def __init__(self):
        t = Transistor()

        inputs = [t.base]
        outputs = [t.collector_output]

        super(Not, self).__init__(inputs, outputs)

    def __str__(self):
        return "Not: input = {}, output = {}".format(self.input, self.output)
        
class And(Base, TwoInputMixin, OneOutputMixin):
    def __init__(self):
        t1 = Transistor()
        t2 = Transistor(connect_to_power = False)
        
        input_a = t1.base
        input_b = t2.base
        inputs = [input_a, input_b]
        
        t1.emitter.connect(t2.collector)
        
        outputs = [t2.emitter]

        super(And, self).__init__(inputs, outputs)

    def __str__(self):
        return "And: input_a = {}, input_b = {}, output = {}".format(self.input_a, self.input_b, self.output)

class Or(Base, TwoInputMixin, OneOutputMixin):
    def __init__(self):
        t1 = Transistor()
        t2 = Transistor()

        input_a = t1.base
        input_b = t2.base
        inputs = [input_a, input_b]

        #join the 2 transmitter emitters
        join = Join(t1.emitter, t2.emitter)
        
        outputs = [join.output]
        
        super(Or, self).__init__(inputs, outputs)

    def __str__(self):
        return "Or: input_a = {}, input_b = {}, output = {}".format(self.input_a, self.input_b, self.output)

class Xor(Base, TwoInputMixin, OneOutputMixin):
    def __init__(self):
        #create gates
        a1 = And()
        o = Or()
        n = Not()
        a2 = And()

        #split input a and b to go to the and1 and or gate 
        input_a = Split(a1.input_a, o.input_a).input
        input_b = Split(a1.input_b, o.input_b).input
        inputs = [input_a, input_b]

        #output of and2 to not
        a1.output.connect(n.input)
        
        #output of not to and2
        n.output.connect(a2.input_a)
        
        #output of or to and2
        o.output.connect(a2.input_b)
        
        #output is the result of and2
        outputs = [a2.output]

        super(Xor, self).__init__(inputs, outputs)

    def __str__(self):
        return "Xor: input_a = {}, input_b = {}, output = {}".format(self.input_a, self.input_b, self.output)

