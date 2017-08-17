from interfaces import Interface
from components import Split
from logicgates import Not, And, Not, Or
from mixins import TwoInputMixin, FourInputMixin, OneOutputMixin, FourOutputMixin

class TwoToOneMultiplexer(Interface, TwoInputMixin, OneOutputMixin):
    def __init__(self):
        n = Not()
        a1 = And()
        a2 = And()
        o = Or()

        #create inputs 
        inputs = {}
        inputs["input_a"] = a1.input_a
        inputs["input_b"] = a2.input_a
        signal_split = Split(n.input, a2.input_b)
        inputs["signal"] = signal_split.input
        
        #connect up gates 
        n.output.connect(a1.input_b)
        a1.output.connect(o.input_a)
        a2.output.connect(o.input_b)

        #create output
        outputs = {}
        outputs["output"] = o.output

        super(TwoToOneMultiplexer, self).__init__(inputs, outputs)

    @property
    def signal(self):
        return self.inputs["signal"]

    def __str__(self):
        return "Two To One Multiplexer: " + super(TwoToOneMultiplexer, self).__str__()

class FourToOneMultiplexer(Interface, FourInputMixin, OneOutputMixin):
    def __init__(self):
        mp1 = TwoToOneMultiplexer()
        mp2 = TwoToOneMultiplexer()
        mp3 = TwoToOneMultiplexer()
        
        inputs = {}
        inputs["input_a"] = mp1.input_a
        inputs["input_b"] = mp1.input_b
        inputs["input_c"] = mp2.input_a
        inputs["input_d"] = mp2.input_b

        mp1.output.connect(mp3.input_a)
        mp2.output.connect(mp3.input_b)

        signal_a_split = Split(mp1.signal, mp2.signal)

        inputs["signal_a"] = signal_a_split.input
        inputs["signal_b"] = mp3.signal

        #inputs = [input_a, input_b, input_c, input_d, signal_a, signal_b]
        outputs = {}
        outputs["output"] = mp3.output

        super(FourToOneMultiplexer, self).__init__(inputs, outputs)

    @property
    def signal_a(self):
        return self.inputs["signal_a"]

    @property
    def signal_b(self):
        return self.inputs["signal_b"]

    def __str__(self):
        return "Four To One Multiplexer: " + super(FourToOneMultiplexer, self).__str__()

class TwoToFourDecoder(Interface, TwoInputMixin, FourOutputMixin):
    def __init__(self):
        n1 = Not()
        n2 = Not()
        a1 = And()
        a2 = And()
        a3 = And()
        a4 = And()

        inputs = {}

        a_split = Split(n1.input, a2.input_a, a4.input_b)
        inputs["input_a"] = a_split.input

        b_split = Split(n2.input, a3.input_a, a4.input_a)
        inputs["input_b"] = b_split.input

        n1_split = Split(a1.input_a, a3.input_b)
        n1.output.connect(n1_split.input)

        n2_split = Split(a1.input_b, a2.input_b)
        n2.output.connect(n2_split.input)

        outputs = {}
        outputs["output_a"] = a1.output
        outputs["output_b"] = a2.output
        outputs["output_c"] = a3.output
        outputs["output_d"] = a4.output

        super(TwoToFourDecoder, self).__init__(inputs, outputs)

    def __str__(self):
        return "Two To Four Decoder: " + super(TwoToFourDecoder, self).__str__()
        