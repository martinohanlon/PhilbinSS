from interfaces import Interface
from components import Transistor, Power, Join, Split
from mixins import InputMixin, InputAMixin, InputBMixin, OutputMixin

class Not(Interface, InputMixin, OutputMixin):
    """
    The implementation of a Not gate, it accepts a single input and has a single output 
    """
    def __init__(self):
        t = Transistor()

        inputs = {}
        outputs = {}

        inputs["input"] = t.base
        outputs["output"] = t.collector_output

        super(Not, self).__init__(inputs, outputs)

    def __str__(self):
        return "Not: " + super(Not, self).__str__()

class And(Interface, InputAMixin, InputBMixin, OutputMixin):
    """
    The implementation of an And gate, it accepts a two inputs and has a single output 
    """
    def __init__(self):
        t1 = Transistor()
        t2 = Transistor(connect_to_power = False)
        
        inputs = {}
        inputs["input_a"] = t1.base
        inputs["input_b"] = t2.base
        
        t1.emitter.connect(t2.collector)
        
        outputs = {}
        outputs["output"] = t2.emitter

        super(And, self).__init__(inputs, outputs)

    def __str__(self):
        return "And: " + super(And, self).__str__()

class Or(Interface, InputAMixin, InputBMixin, OutputMixin):
    """
    The implementation of an Or gate, it accepts a two inputs and has a single output 
    """
    def __init__(self):
        t1 = Transistor()
        t2 = Transistor()

        inputs = {}
        inputs["input_a"] = t1.base
        inputs["input_b"] = t2.base
        
        #join the 2 transmitter emitters
        join = Join(t1.emitter, t2.emitter)
        
        outputs = {}
        outputs["output"] = join.output
        
        super(Or, self).__init__(inputs, outputs)

    def __str__(self):
        return "Or: " + super(Or, self).__str__()

class Xor(Interface, InputAMixin, InputBMixin, OutputMixin):
    """
    The implementation of an Xor gate, it accepts a two inputs and has a single output 
    """
    def __init__(self):
        #create gates
        a1 = And()
        o = Or()
        n = Not()
        a2 = And()

        #split input a and b to go to the and1 and or gate
        inputs = {}
        inputs["input_a"] = Split(a1.input_a, o.input_a).input
        inputs["input_b"] = Split(a1.input_b, o.input_b).input

        #output of and2 to not
        a1.output.connect(n.input)
        
        #output of not to and2
        n.output.connect(a2.input_a)
        
        #output of or to and2
        o.output.connect(a2.input_b)
        
        #output is the result of and2
        outputs = {}
        outputs["output"] = a2.output

        super(Xor, self).__init__(inputs, outputs)

    def __str__(self):
        return "Xor: " + super(Xor, self).__str__()
