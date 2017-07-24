from components import Base, Split
from logicgates import Not, And, Not, Or
from mixins import TwoInputMixin, FourInputMixin, OneOutputMixin, FourOutputMixin

class TwoToOneMultiplexer(Base, TwoInputMixin, OneOutputMixin):
    def __init__(self):
        n = Not()
        a1 = And()
        a2 = And()
        o = Or()

        #create inputs 
        input_a = a1.input_a
        input_b = a2.input_a
        signal_split = Split(n.input, a2.input_b)
        signal = signal_split.input
        inputs = [input_a, input_b, signal]
        
        #connect up gates 
        n.output.connect(a1.input_b)
        a1.output.connect(o.input_a)
        a2.output.connect(o.input_b)

        #create output
        outputs = [o.output]

        super(TwoToOneMultiplexer, self).__init__(inputs, outputs)

    @property
    def signal(self):
        return self.inputs[2]

    def __str__(self):
        return "Two To One Multiplexer: input_a = {}, input_b = {}, signal = {}, output = {}".format(self.input_a, self.input_b, self.signal, self.output)

class FourToOneMultiplexer(Base, FourInputMixin, OneOutputMixin):
    def __init__(self):
        mp1 = TwoToOneMultiplexer()
        mp2 = TwoToOneMultiplexer()
        mp3 = TwoToOneMultiplexer()
        
        input_a = mp1.input_a
        input_b = mp1.input_b
        input_c = mp2.input_a
        input_d = mp2.input_b

        mp1.output.connect(mp3.input_a)
        mp2.output.connect(mp3.input_b)

        signal_a_split = Split(mp1.signal, mp2.signal)

        signal_a = signal_a_split.input
        signal_b = mp3.signal

        inputs = [input_a, input_b, input_c, input_d, signal_a, signal_b]
        outputs = [mp3.output]

        super(FourToOneMultiplexer, self).__init__(inputs, outputs)

    @property
    def signal_a(self):
        return self.inputs[4]

    @property
    def signal_b(self):
        return self.inputs[5]

    def __str__(self):
        return "Four To One Multiplexer: input_a = {}, input_b = {}, input_c = {}, input_d = {}, signal_a = {}, signal_b = {} output = {}".format(self.input_a, self.input_b, self.input_c, self.input_d, self.signal_a ,self.signal_b, self.output)

class TwoToFourDecorder(Base, TwoInputMixin, FourOutputMixin):
    n1 = Not()
    n2 = Not()
    a1 = And()
    a2 = And()
    a3 = And()
    a4 = And()

    a_split = Split(n1.input, a2.input_a, a4.input_b)
    input_a = a_split.input

    b_split = Split(n2.input, a3.input_a, a4.input_a)
    input_b = b_split.input

