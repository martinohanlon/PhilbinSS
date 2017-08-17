from interfaces import Interface
from primitives import Cathode
from components import Split, Transistor
from logicgates import Or, Not, And
from mixins import InputSetMixin, InputResetMixin, InputDataMixin, InputWriteMixin, InputDataEightBitMixin, InputWriteMixin, OutputMixin, OutputEightBitMixin

class AndOrLatch(Interface, InputSetMixin, InputResetMixin, OutputMixin):
    def __init__(self):
        o = Or()
        a = And()
        n = Not()
        
        inputs = {}
        inputs["set"] = o.input_b
        inputs["reset"] = n.input
        
        outputs = {}
        output = Cathode()
        outputs["output"] = output

        o.output.connect(a.input_a)
        n.output.connect(a.input_b)

        a_output_split = Split()
        a.output.connect(a_output_split.input)
        a_output_split.connect(o.input_a)
        a_output_split.connect(output)

        super(AndOrLatch, self).__init__(inputs, outputs)

    def __str__(self):
        return "And Or Latch: " + super(AndOrLatch, self).__str__()
        
class GatedLatch(Interface, InputDataMixin, InputWriteMixin, OutputMixin):
    def __init__(self):

        data_split = Split()
        write_split = Split()
        
        inputs = {}
        inputs["data"] = data_split.input
        inputs["write"] = write_split.input
        
        outputs = {}
        output = Cathode()
        outputs["output"] = output

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
        return "Gated Latch: " + super(GatedLatch, self).__str__()
        
class RAMCell(Interface):
    def __init__(self):
        a1 = And()
        a2 = And()
        a3 = And()
        t = Transistor(connect_to_power = False)
        gl = GatedLatch()

        #wire up row and col selector
        row = a1.input_a
        col = a1.input_b
        a1_split = Split(a2.input_b, a3.input_a)
        a1.output.connect(a1_split.input)

        #write / read enable inputs
        write_enable = a2.input_a
        read_enable = a3.input_b

        #wire up gated latch inputs
        a2.output.connect(gl.write)
        data_in = gl.data

        inputs = {}
        inputs["row"] = row
        inputs["col"] = col
        inputs["write_enable"] = write_enable
        inputs["read_enable"] = read_enable
        inputs["data_in"] = data_in

        #wire up the data out transistor
        gl.output.connect(t.collector)
        a3.output.connect(t.base)
        data_out = t.emitter

        outputs = {}
        outputs["data_out"] = data_out

        super(RAMCell, self).__init__(inputs, outputs)

    @property
    def row(self):
        return self.inputs["row"]

    @property
    def col(self):
        return self.inputs["col"]

    @property
    def write_enable(self):
        return self.inputs["write_enable"]

    @property
    def read_enable(self):
        return self.inputs["read_enable"]

    @property
    def data_in(self):
        return self.inputs["data_in"]

    @property
    def data_out(self):
        return self.outputs["data_out"]

    def __str__(self):
        return "RAM Cell: " + super(RAMCell, self).__str__()
        
class EightBitRegister(Interface, InputDataEightBitMixin, InputWriteMixin, OutputEightBitMixin):
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

        inputs = {}
        inputs["write"] = write_split.input
        inputs["data"] = [gl0.data, gl1.data, gl2.data, gl3.data, gl4.data, gl5.data, gl6.data, gl7.data]
        
        outputs = {}
        outputs["output"] = [gl0.output, gl1.output, gl2.output, gl3.output, gl4.output, gl5.output, gl6.output, gl7.output]

        super(EightBitRegister, self).__init__(inputs, outputs)

    def __str__(self):
        return "8 bit register: inputs = {{data = {}, write = {}}}, outputs = {{output = {}}}".format(self.data, self.write, self.output)
