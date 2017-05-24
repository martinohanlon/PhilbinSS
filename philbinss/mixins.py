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

class ThreeInputMixin():
    @property
    def input_a(self):
        return self._inputs[0]

    @property
    def input_b(self):
        return self._inputs[1]

    @property
    def input_c(self):
        return self._inputs[2]

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
