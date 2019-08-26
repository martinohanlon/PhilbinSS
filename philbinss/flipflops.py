from interfaces import Interface
from logicgates import Nor, And, Not, Or, Nand
from components import Split
from primitives import Cathode
from mixins import InputSetMixin, InputResetMixin, InputDMixin, InputJMixin, InputKMixin, InputClockMixin, OutputQ_Mixin, OutputQMixin
from mixins import InputAMixin, InputBMixin, InputCMixin, OutputMixin

class SRFlipFlop(Interface, InputSetMixin, InputResetMixin, OutputQ_Mixin, OutputQMixin):
    """
    The implementation of a SR (set / reset) flip flop 
    """
    def __init__(self):
        inputs = {}
        outputs = {}

        n1 = Nor()
        n2 = Nor()

        inputs["set"] = n1.input_a
        inputs["reset"] = n2.input_b

        output_q_ = Cathode()
        output_q = Cathode()

        n1_split = Split()
        n2_split = Split()

        n1.output.connect(n1_split.input)
        n1_split.connect(n2.input_a)
        n1_split.connect(output_q_)

        n2.output.connect(n2_split.input)
        n2_split.connect(n1.input_b)
        n2_split.connect(output_q)
        
        outputs["output_q_"] = output_q_
        outputs["output_q"] = output_q

        super(SRFlipFlop, self).__init__(inputs, outputs)

    def __str__(self):
        return "SRFlipFlop: " + super(SRFlipFlop, self).__str__()

class JKFlipFlop(Interface, InputJMixin, InputKMixin, InputClockMixin, OutputQ_Mixin, OutputQMixin):
    """
    The implementation of a JK flip flop 
    """
    def __init__(self):
        inputs = {}
        outputs = {}

        aj1 = And()
        aj2 = And()
        ak1 = And()
        ak2 = And()
        sr = SRFlipFlop()
        clk_split = Split()
        q_split = Split()
        qsplit = Split()

        #connect up the inputs
        inputs["input_j"] = aj1.input_a
        inputs["clock"] = clk_split.input
        clk_split.connect(aj1.input_b)
        clk_split.connect(ak1.input_a)
        inputs["input_k"] = ak1.input_b

        #connect the 2nd AND gates to the SR flip flop
        aj1.output.connect(aj2.input_b)
        ak1.output.connect(ak2.input_a)

        aj2.output.connect(sr.set)
        ak2.output.connect(sr.reset)

        #connect up the sr outputs
        output_q_ = Cathode()
        output_q = Cathode()
        
        sr.output_q_.connect(q_split.input)
        q_split.connect(aj2.input_a)
        q_split.connect(output_q_)

        sr.output_q.connect(qsplit.input)
        qsplit.connect(ak2.input_b)
        qsplit.connect(output_q)

        outputs["output_q_"] = output_q_
        outputs["output_q"] = output_q

        super(JKFlipFlop, self).__init__(inputs, outputs)

    def __str__(self):
        return "JKFlipFlop: " + super(JKFlipFlop, self).__str__()


class ThreeInputNand(Interface, InputAMixin, InputBMixin, InputCMixin, OutputMixin):
    """
    The implementation of a Nand gate, it accepts a three inputs and has a single output 
    """
    def __init__(self):
        a1 = And()
        a2 = And()
        n = Not()

        inputs = {}
        inputs["input_a"] = a1.input_a
        inputs["input_b"] = a1.input_b
        inputs["input_c"] = a2.input_a

        a1.output.connect(a2.input_b)
        
        a2.output.connect(n.input)
        
        outputs = {}
        outputs["output"] = n.output
        
        super(ThreeInputNand, self).__init__(inputs, outputs)

    def __str__(self):
        return "ThreeInputNand: " + super(ThreeInputNand, self).__str__()

class MasterSlaveJKFlipFlop(Interface, InputJMixin, InputKMixin, InputClockMixin, OutputQ_Mixin, OutputQMixin):
    """
    The implementation of a JK flip flop 
    """
    def __init__(self):
        inputs = {}
        outputs = {}

        n1 = ThreeInputNand()
        n2 = ThreeInputNand()
        n3 = Nand()
        n4 = Nand()
        n5 = Nand()
        n6 = Nand()
        n7 = Nand()
        n8 = Nand()
        n = Not()

        clk_split = Split()
        n3_split = Split()
        n4_split = Split()
        n_split = Split()
        n7_split = Split()
        n8_split = Split()

        output_q_ = Cathode()
        output_q = Cathode()

        self.components = {}
        self.components["clk_split"] = clk_split
        self.components["n3_split"] = n3_split
        self.components["n4_split"] = n4_split
        self.components["n_split"] = n_split

        # inputs
        inputs["input_j"] = n1.input_b
        inputs["clock"] = clk_split.input
        inputs["input_k"] = n2.input_b

        # clock split
        clk_split.connect(n1.input_c)
        clk_split.connect(n2.input_a)
        clk_split.connect(n.input)

        # nand 1
        n1.output.connect(n3.input_a)

        # nand 2
        n2.output.connect(n4.input_b)

        # nand 3
        n3.output.connect(n3_split.input)

        # nand 4
        n4.output.connect(n4_split.input)

        # not
        n.output.connect(n_split.input)

        # nand 3 split
        n3_split.connect(n4.input_a)
        n3_split.connect(n5.input_a)

        # nand 4 split
        n4_split.connect(n3.input_b)
        n4_split.connect(n6.input_b)

        # not split
        n_split.connect(n5.input_b)
        n_split.connect(n6.input_a)

        # nand 5
        n5.output.connect(n7.input_a)

        # nand 6
        n6.output.connect(n8.input_b)

        # nand 7
        n7.output.connect(n7_split.input)

        # nand 8
        n8.output.connect(n8_split.input)

        # nand 7 split
        n7_split.connect(n8.input_a)
        n7_split.connect(output_q)
        n7_split.connect(n2.input_c)
        
        # nand 8 split
        n8_split.connect(n7.input_b)
        n8_split.connect(output_q_)
        n8_split.connect(n1.input_a)
        
        outputs["output_q_"] = output_q_
        outputs["output_q"] = output_q

        super(MasterSlaveJKFlipFlop, self).__init__(inputs, outputs)

    def __str__(self):
        return "MasterSlaveJKFlipFlop: " + super(MasterSlaveJKFlipFlop, self).__str__()


class DFlipFlop(Interface, InputDMixin, InputClockMixin, OutputQ_Mixin, OutputQMixin):
    """
    The implementation of a D flip flop 
    """
    def __init__(self):
        inputs = {}
        outputs = {}

        n = Not()
        a1 = And()
        a2 = And()
        sr = SRFlipFlop()
        clk_split = Split()
        d_split = Split()

        #connect up the inputs
        inputs["input_d"] = d_split.input
        d_split.connect(n.input)
        d_split.connect(a2.input_b)
        n.output.connect(a1.input_a)

        inputs["clock"] = clk_split.input
        clk_split.connect(a1.input_b)
        clk_split.connect(a2.input_a)

        a1.output.connect(sr.set)
        a2.output.connect(sr.reset)

        outputs["output_q_"] = sr.output_q_
        outputs["output_q"] = sr.output_q

        super(DFlipFlop, self).__init__(inputs, outputs)

    def __str__(self):
        return "DFlipFlop: " + super(DFlipFlop, self).__str__()
