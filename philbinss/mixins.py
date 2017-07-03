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

class FourInputMixin(object):
    @property
    def input_a(self):
        return self._inputs[0]

    @property
    def input_b(self):
        return self._inputs[1]

    @property
    def input_c(self):
        return self._inputs[2]

    @property
    def input_d(self):
        return self._inputs[3]

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

    def set_bit(self, bit, value):
        self._bits[bit] = value

    def get_bit(self, bit):
        return self._bits[bit]

    @property
    def bit0(self):
        return self._bits[0]

    @bit0.setter
    def bit0(self, value):
        self._bits[0] = value

    @property
    def bit1(self):
        return self._bits[1]

    @bit1.setter
    def bit1(self, value):
        self._bits[1] = value

    @property
    def bit2(self):
        return self._bits[2]

    @bit2.setter
    def bit2(self, value):
        self._bits[2] = value

    @property
    def bit3(self):
        return self._bits[3]

    @bit3.setter
    def bit3(self, value):
        self._bits[3] = value

    @property
    def bit4(self):
        return self._bits[4]

    @bit4.setter
    def bit4(self, value):
        self._bits[4] = value

    @property
    def bit5(self):
        return self._bits[5]
    
    @bit5.setter
    def bit5(self, value):
        self._bits[5] = value

    @property
    def bit6(self):
        return self._bits[6]

    @bit6.setter
    def bit6(self, value):
        self._bits[6] = value

    @property
    def bit7(self):
        return self._bits[7]
    
    @bit7.setter
    def bit7(self, value):
        self._bits[7] = value

    def get_int(self):
        #there must be a better way of converting binary to int
        multiplier = 1
        int_value = 0
        for bit in self._bits:
            if bit.value:
                int_value += multiplier
            multiplier = multiplier * 2
        
        return int_value

    @property
    def int_value(self):
        return self.get_int()


class TwoEightBitInputMixin(object):
    @property
    def input_a(self):
        return EightBit(self._inputs[0])

    @property
    def input_b(self):
        return EightBit(self._inputs[1])

class OneEightBitOutputMixin(object):
    @property
    def sum(self):
        return EightBit(self._outputs[0])

class OneEightBitSumOneCarryOutputMixin(object):
    @property
    def sum(self):
        return EightBit(self._outputs[0])

    @property
    def carry(self):
        return self._outputs[1]

