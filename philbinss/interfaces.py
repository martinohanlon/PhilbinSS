
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
