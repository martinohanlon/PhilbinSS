from interfaces import Interface
from logicgates import Nor
from components import Split
from primitives import Cathode
from mixins import InputSetMixin, InputResetMixin, OutputAMixin, OutputBMixin

class SRFlipFlop(Interface, InputSetMixin, InputResetMixin, OutputAMixin, OutputBMixin):
    """
    The implementation of a SR (set / reset) flip flop 
    """
    def __init__(self):
        inputs = {}
        outputs = {}

        x1 = Nor()
        x2 = Nor()

        inputs["set"] = x1.input_a
        inputs["reset"] = x2.input_b

        output_a = Cathode()
        output_b = Cathode()

        x1_split = Split()
        x2_split = Split()

        x1.output.connect(x1_split.input)
        x1_split.connect(x2.input_a)
        x1_split.connect(output_a)

        x2.output.connect(x2_split.input)
        x2_split.connect(x1.input_b)
        x2_split.connect(output_b)
        
        outputs["output_a"] = output_a
        outputs["output_b"] = output_b

        super(SRFlipFlop, self).__init__(inputs, outputs)

    def __str__(self):
        return "SRFlipFlop: " + super(SRFlipFlop, self).__str__()
