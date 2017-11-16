from interfaces import Interface
from logicgates import And, Xor, Or
from components import Split, Power, MultiPower
from primitives import Cathode
from flipflops import JKFlipFlop
from mixins import InputAMixin, InputBMixin, InputCMixin, InputOperatorMixin, OutputSumMixin, OutputCarryMixin, InputAEightBitMixin, InputBEightBitMixin, OutputSumEightBitMixin, OutputCarryMixin, InputClockMixin, OutputEightBitMixin

class HalfAdder(Interface, InputAMixin, InputBMixin, OutputSumMixin, OutputCarryMixin):
    def __init__(self):
        x = Xor()
        a = And()

        #split input a and b to go to the xor and and gate 
        inputs = {}
        inputs["input_a"] = Split(x.input_a, a.input_a).input
        inputs["input_b"] = Split(x.input_b, a.input_b).input
        
        #get the output from the xor and and gates
        outputs = {}
        outputs["sum"] = x.output
        outputs["carry"] = a.output

        super(HalfAdder, self).__init__(inputs, outputs)

    def __str__(self):
        return "HalfAdder: " + super(HalfAdder, self).__str__()

class FullAdder(Interface, InputAMixin, InputBMixin, InputCMixin, OutputSumMixin, OutputCarryMixin):
    def __init__(self):
        ha1 = HalfAdder()
        ha2 = HalfAdder()
        o = Or()

        #create inputs
        inputs = {}
        inputs["input_a"] = ha1.input_a
        inputs["input_b"] = ha1.input_b
        inputs["input_c"] = ha2.input_b

        #connect ha1 carry to ha2 input_a
        ha1.sum.connect(ha2.input_a)

        #connect the carrys to the or
        ha1.carry.connect(o.input_a)
        ha2.carry.connect(o.input_b)

        #connect the outputs
        outputs = {}
        outputs["sum"] = ha2.sum
        outputs["carry"] = o.output

        super(FullAdder, self).__init__(inputs, outputs)

    def __str__(self):
        return "FullAdder: " + super(FullAdder, self).__str__()

class EightBitRippleCarryAdder(Interface, InputAEightBitMixin, InputBEightBitMixin, OutputSumEightBitMixin, OutputCarryMixin):
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
        inputs = {}
        inputs["input_a"] = [ha.input_a, fa1.input_b, fa2.input_b, fa3.input_b, fa4.input_b, fa5.input_b, fa6.input_b, fa7.input_b]
        inputs["input_b"] = [ha.input_b, fa1.input_c, fa2.input_c, fa3.input_c, fa4.input_c, fa5.input_c, fa6.input_c, fa7.input_c]
        
        outputs = {}
        outputs["sum"] = [ha.sum, fa1.sum, fa2.sum, fa3.sum, fa4.sum, fa5.sum, fa6.sum, fa7.sum]
        outputs["carry"] = fa7.carry

        #connect up adders
        ha.carry.connect(fa1.input_a)
        fa1.carry.connect(fa2.input_a)
        fa2.carry.connect(fa3.input_a)
        fa3.carry.connect(fa4.input_a)
        fa4.carry.connect(fa5.input_a)
        fa5.carry.connect(fa6.input_a)
        fa6.carry.connect(fa7.input_a)

        super(EightBitRippleCarryAdder, self).__init__(inputs, outputs)

    def __str__(self):
        return "EightBitRippleCarryAdder: inputs = {{input_a = {}, input_b = {}}}, outputs = {{sum = {}, carry = {}}}".format(self.input_a, self.input_b, self.sum, self.carry)

class EightBitRippleCarryAdderSubtractor(Interface, InputAEightBitMixin, InputBEightBitMixin, InputOperatorMixin, OutputSumEightBitMixin, OutputCarryMixin):
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
        inputs = {}
        inputs["operator"] = op_split.input
        inputs["input_a"] = [fa0.input_b, fa1.input_b, fa2.input_b, fa3.input_b, fa4.input_b, fa5.input_b, fa6.input_b, fa7.input_b]
        inputs["input_b"] = [xo0.input_b, xo1.input_b, xo2.input_b, xo3.input_b, xo4.input_b, xo5.input_b, xo6.input_b, xo7.input_b]
        
        outputs = {}
        outputs["sum"] = [fa0.sum, fa1.sum, fa2.sum, fa3.sum, fa4.sum, fa5.sum, fa6.sum, fa7.sum]
        outputs["carry"] = fa7.carry
        
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

    def __str__(self):
        return "EightBitRippleCarryAdderSubtractor: inputs = {{input_a = {}, input_b = {}, operator = {}}}, outputs = {{sum = {}, carry = {}}}".format(self.input_a, self.input_b, self.operator, self.sum, self.carry)


class ALU(Interface, InputAEightBitMixin, InputBEightBitMixin, InputOperatorMixin, OutputSumEightBitMixin, OutputCarryMixin):
    def __init__(self):
        """
        Truth table for overflow

        op carry overflow
        1  1     0
        1  0     1
        0  0     0
        0  1     1

        Truth table for negative

        op overflow negative
        1  1        1
        1  0        0
        0  1        0
        0  0        0

        operator:
        '0' - addition
        '1' - subtraction
        """
        rcas = EightBitRippleCarryAdderSubtractor()
        overflow_xor = Xor()
        neg_and = And()
        
        #op input
        #send the op code to the rcas, the overflow xor and the negative and
        op_split = Split(rcas.operator, overflow_xor.input_a, neg_and.input_a)
        op = op_split.input
        
        inputs = {}
        inputs["input_a"] = rcas.input_a.bits
        inputs["input_b"] = rcas.input_b.bits
        inputs["operator"] = op
#        inputs = [rcas.input_a.bits, rcas.input_b.bits, op]

        #carry output
        #send the rcas carry to the carry output and the overflow xor
        carry = Cathode()  
        carry_split = Split(carry, overflow_xor.input_b)
        rcas.carry.connect(carry_split.input)

        #overflow output
        #send the overflow to the overflow output and the negative And
        overflow = Cathode()
        overflow_split = Split(overflow, neg_and.input_b)
        overflow_xor.output.connect(overflow_split.input)
        
        #negative output
        negative = neg_and.output

        outputs = {}
        outputs["sum"] = rcas.sum.bits
        outputs["carry"] = rcas.carry
        outputs["overflow"] = overflow
        outputs["negative"] = negative
        #outputs = [rcas.sum.bits, rcas.carry, overflow, negative]

        super(ALU, self).__init__(inputs, outputs)

    #output flags    
    @property
    def overflow(self):
        return self.outputs["overflow"]

    @property
    def negative(self):
        """
        '0' - positive
        '1' - negative
        """
        return self.outputs["negative"]

    def __str__(self):
        return "ALU: inputs = {{input_a = {}, input_b = {}, operator = {}}}, outputs = {{sum = {}, carry = {}, overflow = {}, negative = {}}}".format(self.input_a, self.input_b, self.operator, self.sum, self.carry, self.overflow, self.negative)

class EightBitRippleCounter(Interface, InputClockMixin, OutputEightBitMixin):
    def __init__(self):
        inputs = {}
        outputs = {}

        power = MultiPower()
        power.on()

        # create jks and output cathodes
        jks = []            
        output_cathodes = []
        for i in range(8):
            # create jk
            jk = JKFlipFlop()
            jks.append(jk)
            # connect up flip flops J K to power
            power.connect(jk.input_j)
            #power.connect(jk.input_k)
            #create output cathode
            output_cathodes.append(Cathode())

        # connect up q's to output and next jk's clock
        for i in range(0,7):
            q_split = Split(jks[i + 1].clock, output_cathodes[i])
            jks[i].output_q.connect(q_split.input)

        # connect up final jk
        jks[7].output_q.connect(output_cathodes[7])

        inputs["clock"] = jks[0].clock
        outputs["output"] = output_cathodes

        super(EightBitRippleCounter, self).__init__(inputs, outputs)

    def __str__(self):
        return "EightBitRippleCounter: inputs = {{clock = {}}}, outputs = {{output = {}}}".format(self.clock, self.output)
