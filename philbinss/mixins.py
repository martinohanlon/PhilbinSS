from interfaces import FourBit, EightBit

class InputMixin(object):
    @property
    def input(self):
        return self._inputs["input"]

class InputAMixin(object):
    @property
    def input_a(self):
        return self._inputs["input_a"]

class InputBMixin(object):
    @property
    def input_b(self):
        return self._inputs["input_b"]

class InputCMixin(object):
    @property
    def input_c(self):
        return self._inputs["input_c"]

class InputDMixin(object):
    @property
    def input_d(self):
        return self._inputs["input_d"]

class InputSetMixin(object):
    @property
    def set(self):
        return self._inputs["set"]

class InputResetMixin(object):
    @property
    def reset(self):
        return self._inputs["reset"]

class InputDataMixin(object):
    @property
    def data(self):
        return self._inputs["data"]

class InputWriteMixin(object):
    @property
    def write(self):
        return self._inputs["write"]

class InputDataEightBitMixin(object):
    @property
    def data(self):
        return EightBit(self._inputs["data"])

class InputAEightBitMixin(object):
    @property
    def input_a(self):
        return EightBit(self._inputs["input_a"])

class InputBEightBitMixin(object):
    @property
    def input_b(self):
        return EightBit(self._inputs["input_b"])

class InputWriteMixin(object):
    @property
    def write(self):
        return self._inputs["write"]

class InputWriteEnableMixin(object):
    @property
    def write_enable(self):
        return self.inputs["write_enable"]

class InputReadEnableMixin(object):
    @property
    def read_enable(self):
        return self.inputs["read_enable"]

class InputDataInMixin(object):
    @property
    def data_in(self):
        return self.inputs["data_in"]

class InputOperatorMixin(object):
    @property
    def operator(self):
        return self._inputs["operator"]

class InputAddressFourBitMixin(object):
    @property
    def address(self):
        return FourBit(self.inputs["address"])

class OutputMixin(object):
    @property
    def output(self):
        return self._outputs["output"]

class OutputAMixin(object):
    @property
    def output_a(self):
        return self._outputs["output_a"]

class OutputBMixin(object):
    @property
    def output_b(self):
        return self._outputs["output_b"]

class OutputCMixin(object):
    @property
    def output_c(self):
        return self._outputs["output_c"]

class OutputDMixin(object):
    @property
    def output_d(self):
        return self._outputs["output_d"]

class OutputSumMixin(object):
    @property
    def sum(self):
        return self._outputs["sum"]

class OutputCarryMixin(object):
    @property
    def carry(self):
        return self._outputs["carry"]

class OutputEightBitMixin(object):
    @property
    def output(self):
        return EightBit(self._outputs["output"])

class OutputSumEightBitMixin(object):
    @property
    def sum(self):
        return EightBit(self._outputs["sum"])

class OutputDataOutMixin(object):
    @property
    def data_out(self):
        return self.outputs["data_out"]
