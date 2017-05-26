class OneInputMixin(object):
    @property
    def input(self):
        return self._inputs[0]

class TwoInputMixin(object):
    @property
    def input_a(self):
        return self._inputs[0]

    @property
    def input_b(self):
        return self._inputs[1]

class ThreeInputMixin(object):
    @property
    def input_a(self):
        return self._inputs[0]

    @property
    def input_b(self):
        return self._inputs[1]

    @property
    def input_c(self):
        return self._inputs[2]

class OneOutputMixin(object):
    @property
    def output(self):
        return self._outputs[0]

class SumCarryOuputMixin(object):
    @property
    def sum(self):
        return self._outputs[0]

    @property
    def carry(self):
        return self._outputs[1]

class EightBit(object):
    def __init__(self, bits):
        if len(bits) != 8:
            raise ValueError("there must be 8 bits - {} given".format(len(bits)))
        self._bits = bits

    @property
    def bit0(self):
        return self._bits[0]
    
    @property
    def bit1(self):
        return self._bits[1]
    
    @property
    def bit2(self):
        return self._bits[2]
    
    @property
    def bit3(self):
        return self._bits[3]
    
    @property
    def bit4(self):
        return self._bits[4]
    
    @property
    def bit5(self):
        return self._bits[5]
    
    @property
    def bit6(self):
        return self._bits[6]
    
    @property
    def bit7(self):
        return self._bits[7]
    
class TwoEightBitInputMixin(object):
    @property
    def input_a(self):
        return EightBit(self._inputs[0])

    @property
    def input_b(self):
        return EightBitt(self._inputs[1])

class OneEightBitOutputMixin(object):
    @property
    def output(self):
        return EightBit(self._outputs)
