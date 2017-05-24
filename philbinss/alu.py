from logicgates import And, Xor, Or
from components import Split
from mixins import InputOutputMixin, TwoInputMixin, ThreeInputMixin, SumCarryOuputMixin

class HalfAdder(InputOutputMixin, TwoInputMixin, SumCarryOuputMixin):
    def __init__(self):
        x = Xor()
        a = And()

        #split input a and b to go to the xor and and gate 
        input_a = Split(x.input_a, a.input_a).input
        input_b = Split(x.input_b, a.input_b).input
        inputs = [input_a, input_b]

        #get the output from the xor and and gates
        thesum = x.output
        carry = a.output
        outputs = [thesum, carry]

        super(HalfAdder, self).__init__(inputs, outputs)

    def __str__(self):
        return "HalfAdder: input_a = {}, input_b = {}, carry = {}, sum = {}".format(self.input_a, self.input_b, self.sum, self.carry)

class FullAdder(InputOutputMixin, ThreeInputMixin, SumCarryOuputMixin):
    def __init__(self):
        ha1 = HalfAdder()
        ha2 = HalfAdder()
        o = Or()

        #create inputs
        input_a = ha1.input_a
        input_b = ha1.input_b
        input_c = ha2.input_b
        inputs = [input_a, input_b, input_c]

        #connect ha1 carry to ha2 input_a
        ha1.sum.connect(ha2.input_a)

        #connect the carrys to the or
        ha1.carry.connect(o.input_a)
        ha2.carry.connect(o.input_b)

        #connect the outputs
        thesum = ha2.sum
        carry = o.output
        outputs = [thesum, carry]

        super(FullAdder, self).__init__(inputs, outputs)

    def __str__(self):
        return "FullAdder: input_a = {}, input_b = {}, input_c = {}, carry = {}, sum = {}".format(self.input_a, self.input_b, self.input_c, self.sum, self.carry)
