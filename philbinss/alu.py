from logicgates import And, Xor
from components import Split

class InputOutputMixin():
    def __init__(self, inputs, outputs):
        self._inputs = inputs
        self._outputs = outputs

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    def __repr__(self):
        return "{},{}".format(self.inputs, self.output)
        
    def __str__(self):
        return "inputs = {}, output = {}".format(self.inputs, self.output)

class TwoInputMixin():
    @property
    def input_a(self):
        return self._inputs[0]

    @property
    def input_b(self):
        return self._inputs[1]

class SumCarryOuputMixin():
    @property
    def sum(self):
        return self._outputs[0]

    @property
    def carry(self):
        return self._outputs[1]

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
