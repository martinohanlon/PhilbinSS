from logicgates import And, Xor, Or
from components import Base, Split, Power
from mixins import TwoInputMixin, ThreeInputMixin, SumCarryOuputMixin, TwoEightBitInputMixin, OneEightBitSumOneCarryOutputMixin

class HalfAdder(Base, TwoInputMixin, SumCarryOuputMixin):
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

class FullAdder(Base, ThreeInputMixin, SumCarryOuputMixin):
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

class EightBitRippleCarryAdder(Base, TwoEightBitInputMixin, OneEightBitSumOneCarryOutputMixin):
    def __init__(self):
        ha = HalfAdder()
        fa1 = FullAdder()
        fa2 = FullAdder()
        fa3 = FullAdder()
        fa4 = FullAdder()
        fa5 = FullAdder()
        fa6 = FullAdder()
        fa7 = FullAdder()
        
        #wire up outputs and inputs
        input_a = [ha.input_a, fa1.input_b, fa2.input_b, fa3.input_b, fa4.input_b, fa5.input_b, fa6.input_b, fa7.input_b]
        input_b = [ha.input_b, fa1.input_c, fa2.input_c, fa3.input_c, fa4.input_c, fa5.input_c, fa6.input_c, fa7.input_c]
        inputs = [input_a, input_b]

        output_sum = [ha.sum, fa1.sum, fa2.sum, fa3.sum, fa4.sum, fa5.sum, fa6.sum, fa7.sum]
        output_carry = fa7.carry
        outputs = [output_sum, output_carry]

        #connect up adders
        ha.carry.connect(fa1.input_a)
        fa1.carry.connect(fa2.input_a)
        fa2.carry.connect(fa3.input_a)
        fa3.carry.connect(fa4.input_a)
        fa4.carry.connect(fa5.input_a)
        fa5.carry.connect(fa6.input_a)
        fa6.carry.connect(fa7.input_a)

        super(EightBitRippleCarryAdder, self).__init__(inputs, outputs)

class EightBitRippleCarryAdderSubtractor(Base, TwoEightBitInputMixin, OneEightBitSumOneCarryOutputMixin):
    def __init__(self):
        fa0 = FullAdder()
        fa1 = FullAdder()
        fa2 = FullAdder()
        fa3 = FullAdder()
        fa4 = FullAdder()
        fa5 = FullAdder()
        fa6 = FullAdder()
        fa7 = FullAdder()

        xo0 = Xor()
        xo1 = Xor()
        xo2 = Xor()
        xo3 = Xor()
        xo4 = Xor()
        xo5 = Xor()
        xo6 = Xor()
        xo7 = Xor()

        #send the op to the first full adder and the xors
        op_split = Split(fa0.input_a, xo0.input_a, xo1.input_a, xo2.input_a, xo3.input_a, xo4.input_a, xo5.input_a, xo6.input_a, xo7.input_a)

        #wire up outputs and inputs
        op = op_split.input
        input_a = [fa0.input_b, fa1.input_b, fa2.input_b, fa3.input_b, fa4.input_b, fa5.input_b, fa6.input_b, fa7.input_b]
        input_b = [xo0.input_b, xo1.input_b, xo2.input_b, xo3.input_b, xo4.input_b, xo5.input_b, xo6.input_b, xo7.input_b]
        inputs = [input_a, input_b, op]

        output_sum = [fa0.sum, fa1.sum, fa2.sum, fa3.sum, fa4.sum, fa5.sum, fa6.sum, fa7.sum]
        output_carry = fa7.carry
        outputs = [output_sum, output_carry]

        #connect xors to adders
        xo0.output.connect(fa0.input_c)
        xo1.output.connect(fa1.input_c)
        xo2.output.connect(fa2.input_c)
        xo3.output.connect(fa3.input_c)
        xo4.output.connect(fa4.input_c)
        xo5.output.connect(fa5.input_c)
        xo6.output.connect(fa6.input_c)
        xo7.output.connect(fa7.input_c)

        #connect up adders
        fa0.carry.connect(fa1.input_a)
        fa1.carry.connect(fa2.input_a)
        fa2.carry.connect(fa3.input_a)
        fa3.carry.connect(fa4.input_a)
        fa4.carry.connect(fa5.input_a)
        fa5.carry.connect(fa6.input_a)
        fa6.carry.connect(fa7.input_a)

        super(EightBitRippleCarryAdderSubtractor, self).__init__(inputs, outputs)

    @property
    def operator(self):
        return self.inputs[2]