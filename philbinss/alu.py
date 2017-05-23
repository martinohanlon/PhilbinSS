from logicgates import And, Xor
from components import Split
from mixins import InputOutputMixin, TwoInputMixin, SumCarryOuputMixin

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
        return "HalfAdder: input_a = {}, input_b = {}, sum = {} carry = {}".format(self.input_a, self.input_b, self.sum, self.carry)
