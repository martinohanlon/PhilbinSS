from interfaces import Interface
from logicgates import Nor, And
from components import Split
from primitives import Cathode
from mixins import InputSetMixin, InputResetMixin, InputJMixin, InputKMixin, InputClockMixin, OutputQ_Mixin, OutputQMixin

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
