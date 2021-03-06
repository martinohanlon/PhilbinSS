
class Interface(object):
    """
    The base of all components it implements the simplest of Interface, input(s) and output(s)
    """
    def __init__(self, inputs, outputs):
        self._inputs = inputs
        self._outputs = outputs

        #create properties from inputs and outputs
        #for k, v in self._inputs.items():
        #    setattr(self, k, v)
        #for k, v in self._outputs.items():
        #    setattr(self, k, v)

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    def _format_dict(self, thedict):
        value = "{"
        for k, v in thedict.items():
            value += k + " = " + str(v)
            value += ", "
        value = value[:-2]
        value += "}"
        return value
            
    def __str__(self):
        return "inputs = {}, outputs = {}".format(self._format_dict(self.inputs), self._format_dict(self.outputs))

class MultiBit(object):
    def __init__(self, bits):
        self._bits = bits

    @property
    def bits(self):
        return self._bits

    @property
    def length(self):
        return(len(self._bits))

    @property
    def binary_value(self):
        return self.get_binary()

    @property
    def int_value(self):
        """
        Returns the integer value of the bits - useful for testing
        """
        return self.get_int()

    def get_bit(self, bit):
        return self._bits[bit]

    def set_bit(self, bit, value):
        self._bits[bit] = value

    def get_binary(self):
        binary_value = ""
        for bit in self._bits:
            binary_value += "1" if bit.value else "0"
        return binary_value

    def get_int(self):
        #there must be a better way of converting binary to int
        multiplier = 1
        int_value = 0
        for bit in self._bits:
            if bit.value:
                int_value += multiplier
            multiplier = multiplier * 2
        
        return int_value

    def connect(self, multi_bit):
        """
        Connect all the nodes in this multi bit interface to another multi bit interface

        multi_bit: the multi_bit to connect too 
        """
        if self.length != multi_bit.length:
            raise ValueError("expect {} bits - {} given".format(self.length, multi_bit.length))

        for i in range(self.length):
            self.bits[i].connect(multi_bit.bits[i])

    def __str__(self):
        return "{} bit(binary = {}, int = {})".format(self.length, self.binary_value, self.int_value)

class FourBit(MultiBit):
    def __init__(self, bits):
        if len(bits) != 4:
            raise ValueError("there must be 4 bits - {} given".format(len(bits)))
        super(FourBit, self).__init__(bits)

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

class EightBit(MultiBit):
    def __init__(self, bits):
        if len(bits) != 8:
            raise ValueError("there must be 8 bits - {} given".format(len(bits)))
        super(EightBit, self).__init__(bits)

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
