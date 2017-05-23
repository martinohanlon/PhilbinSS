
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
        return "inputs = {}, outputs = {}".format(self.inputs, self.output)

class OneInputMixin():
    @property
    def input(self):
        return self._inputs[0]

class TwoInputMixin():
    @property
    def input_a(self):
        return self._inputs[0]

    @property
    def input_b(self):
        return self._inputs[1]

class OneOutputMixin():
    @property
    def output(self):
        return self._outputs[0]

class SumCarryOuputMixin():
    @property
    def sum(self):
        return self._outputs[0]

    @property
    def carry(self):
        return self._outputs[1]
