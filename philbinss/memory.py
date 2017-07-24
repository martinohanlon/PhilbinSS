from primitives import Cathode
from components import Base, Split
from logicgates import Or, Not, And
from mixins import SetResetInputMixin, DataWriteInputMixin, OneOutputMixin, OneEightBitDataOneWriteInputMixin, OneEightBitOutputMixin

class AndOrLatch(Base, SetResetInputMixin, OneOutputMixin):
    def __init__(self):
        o = Or()
        a = And()
        n = Not()
        
        input_set = o.input_b
        input_reset = n.input
        inputs = [input_set, input_reset]
        
        output = Cathode()
        outputs = [output]

        o.output.connect(a.input_a)
        n.output.connect(a.input_b)

        a_output_split = Split()
        a.output.connect(a_output_split.input)
        a_output_split.connect(o.input_a)
        a_output_split.connect(output)

        super(AndOrLatch, self).__init__(inputs, outputs)

    def __str__(self):
        return "And Or Latch: set = {}, reset = {}, output = {}".format(self.set, self.reset, self.output)

class GatedLatch(Base, DataWriteInputMixin, OneOutputMixin):
    def __init__(self):

        data_split = Split()
        write_split = Split()
        
        input_data = data_split.input
        input_write = write_split.input
        inputs = [input_data, input_write]

        output = Cathode()
        outputs = [output]

        n1 = Not()
        n2 = Not()
        a1 = And()
        a2 = And()
        a3 = And()
        o = Or()

        data_split.connect(a1.input_a)
        data_split.connect(n1.input)

        n1.output.connect(a2.input_a)

        write_split.connect(a1.input_b)
        write_split.connect(a2.input_b)

        a1.output.connect(o.input_b)   
        a2.output.connect(n2.input)

        o.output.connect(a3.input_a)
        n2.output.connect(a3.input_b)

        a_output_split = Split()
        a3.output.connect(a_output_split.input)
        a_output_split.connect(o.input_a)
        a_output_split.connect(output)

        super(GatedLatch, self).__init__(inputs, outputs)

    def __str__(self):
        return "Gated Latch: data = {}, write = {}, output = {}".format(self.data, self.write, self.output)

class SelectableGatedLatch(Base):
    def __init__(self):
        pass

class EightBitRegister(Base, OneEightBitDataOneWriteInputMixin, OneEightBitOutputMixin):
    def __init__(self):
        gl0 = GatedLatch()
        gl1 = GatedLatch()
        gl2 = GatedLatch()
        gl3 = GatedLatch()
        gl4 = GatedLatch()
        gl5 = GatedLatch()
        gl6 = GatedLatch()
        gl7 = GatedLatch()
        
        write_split = Split(gl0.write, gl1.write, gl2.write, gl3.write, gl4.write, gl5.write, gl6.write, gl7.write)

        input_write = write_split.input
        input_data = [gl0.data, gl1.data, gl2.data, gl3.data, gl4.data, gl5.data, gl6.data, gl7.data]
        inputs = [input_data, input_write]

        output_data = [gl0.output, gl1.output, gl2.output, gl3.output, gl4.output, gl5.output, gl6.output, gl7.output]
        outputs = [output_data]

        super(EightBitRegister, self).__init__(inputs, outputs)

    def __str__(self):
        return "8 bit register: data = {}, write = {}, output = {}".format(self.data, self.write, self.output)
