from interfaces import Interface
from primitives import Cathode
from components import Split, Join, Transistor
from logicgates import Or, Not, And
from multiplexers import TwoToFourDecoder
from mixins import InputSetMixin, InputResetMixin, InputDataMixin, InputWriteMixin, InputDataEightBitMixin, InputDataInEightBitMixin, InputWriteMixin, InputWriteEnableMixin, InputReadEnableMixin, InputDataInMixin, InputAddressFourBitMixin, OutputMixin, OutputEightBitMixin, OutputDataOutMixin, OutputDataOutEightBitMixin

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
        
class RAMCell(Interface, InputWriteEnableMixin, InputReadEnableMixin, InputDataInMixin, OutputDataOutMixin):
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

    def __str__(self):
        return "RAM Cell: " + super(RAMCell, self).__str__()

class SixteenBitMemory(Interface, InputAddressFourBitMixin, InputWriteEnableMixin, InputReadEnableMixin, InputDataInMixin, OutputDataOutMixin):
    def __init__(self):

        # create the memory address
        col_decoder = TwoToFourDecoder()
        row_decoder = TwoToFourDecoder()
        address = [row_decoder.input_a, row_decoder.input_b, col_decoder.input_a, col_decoder.input_b]
        
        write_enable = Split()
        read_enable = Split()
        data_in = Split()
        data_out = Join()

        # create ram cells in a matrix
        # create splits for the address
        row_a_split = Split()
        row_b_split = Split()
        row_c_split = Split()
        row_d_split = Split()
        row_decoder.output_a.connect(row_a_split.input)
        row_decoder.output_b.connect(row_b_split.input)
        row_decoder.output_c.connect(row_c_split.input)
        row_decoder.output_d.connect(row_d_split.input)

        col_a_split = Split()
        col_b_split = Split()
        col_c_split = Split()
        col_d_split = Split()
        col_decoder.output_a.connect(col_a_split.input)
        col_decoder.output_b.connect(col_b_split.input)
        col_decoder.output_c.connect(col_c_split.input)
        col_decoder.output_d.connect(col_d_split.input)

        address_row_outputs = [row_a_split, row_b_split, row_c_split, row_d_split]
        address_col_outputs = [col_a_split, col_b_split, col_c_split, col_d_split]
        
        for row in range(4):
            for col in range(4):
                # create a ram cell and write it up
                ram_cell = RAMCell()
                address_row_outputs[row].connect(ram_cell.row)
                address_col_outputs[col].connect(ram_cell.col)
                read_enable.connect(ram_cell.read_enable)
                write_enable.connect(ram_cell.write_enable)
                data_in.connect(ram_cell.data_in)
                data_out.connect(ram_cell.data_out)

        inputs = {}
        inputs["address"] = address
        inputs["write_enable"] = write_enable.input
        inputs["read_enable"] = read_enable.input
        inputs["data_in"] = data_in.input

        outputs = {}
        outputs["data_out"] = data_out.output

        super(SixteenBitMemory, self).__init__(inputs, outputs)

class SixteenByteMemory(Interface, InputAddressFourBitMixin, InputWriteEnableMixin, InputReadEnableMixin, InputDataInEightBitMixin, OutputDataOutMixin, OutputDataOutEightBitMixin):
    
    def __init__(self):
        # create 8 16 bit memory modules and chain them together
        address_splits = [Split(), Split(), Split(), Split()]
        write_split = Split()
        read_split = Split()

        data_out = []
        data_in = []

        # create and connect up the 16 bit memory modules
        for i in range(8):
            bit = SixteenBitMemory()
            # connect up the address
            for j in range(4):
                address_splits[j].connect(bit.address.get_bit(j))
            # connect write and read enable 
            write_split.connect(bit.write_enable)
            read_split.connect(bit.read_enable)
            # create lists for data in and out
            data_out.append(bit.data_out)
            data_in.append(bit.data_in)

        inputs = {}
        inputs["address"] = [address_splits[0].input, address_splits[1].input, address_splits[2].input, address_splits[3].input]
        inputs["write_enable"] = write_split.input
        inputs["read_enable"] = read_split.input
        inputs["data_in"] = data_in

        outputs = {}
        outputs["data_out"] = data_out

        super(SixteenByteMemory, self).__init__(inputs, outputs)

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
