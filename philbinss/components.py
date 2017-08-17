from interfaces import Interface
from primitives import Anode, Cathode
from mixins import OneInputMixin, OneOutputMixin

class Split(Interface, OneInputMixin):
    """
    A Split is used to split 1 input into many outputs
    """
    def __init__(self, *outputs):
        inputs = {}
        #if the input changes, update the outputs
        inputs["input"] = Cathode(value_changed = self._update_state)

        #create the split with zero outputs 
        super(Split, self).__init__(inputs, {})

        #nodes the split will output to and update 
        self._split_outputs = []

        # connect up the outputs
        for output in outputs:
            self.connect(output)

    def connect(self, output):
        #create an anode which will connect to the output
        anode = Anode()
        anode.connect(output)
        self._split_outputs.append(anode)

        self._update_state()
        
    def _update_state(self):
        for output in self._split_outputs:
            output.value = self.value

    @property
    def value(self):
        return self.input.value

    def __str__(self):
        return "Split: {}".format(self.input)

class Join(Interface, OneOutputMixin):
    """
    A join is used to bring multiple inputs into 1 output
    """
    def __init__(self, *inputs):
        outputs = {}
        outputs["output"] = Anode()

        #create the join with zero inputs 
        super(Join, self).__init__({}, outputs)

        #nodes the join will take values from
        self._join_inputs = []

        #connect the inputs
        for aninput in inputs:
            self.connect(aninput)
    
    def connect(self, aninput):
        #add the input to the connections
        self._join_inputs.append(aninput)
        
        #create and connect cathode to the input
        cathode = Cathode(value_changed = self._update_state)
        aninput.connect(cathode)

        self._update_state()
            
    def _update_state(self):
        self.output.value = self.value
        
    @property
    def value(self):
        #if any node is True, return True, else False
        for aninput in self._join_inputs:
            if aninput.value:
                return True
        return False

    def __str__(self):
        return "Join: {}".format(self.output)

class Power(Anode):
    """
    Power is a an Anode which implements simple ``on()``, ``off()`` methods 
    """
    def __init__(self, on = False):
        super(Power, self).__init__(value = on)

    def on(self):
        self.value = True

    def off(self):
        self.value = False

    def __str__(self):
        return "Power: {}".format(self.value)

class MultiPower(Split):
    """
    A MultiPower is a Split connected up to Anode, it can acceptable multiple connections 
    and like Power implements ``on()`` and ``off()``.
    """
    def __init__(self, on = False):
        super(MultiPower, self).__init__()

        #create the power supply and connect it to the split
        self._supply = Anode(value = on)
        self._supply.connect(self.input)

    @property
    def value(self):
        return self._supply.value

    @value.setter
    def value(self, value):
        self._supply.value = value

    def on(self):
        self._supply.value = True

    def off(self):
        self._supply.value = False

    def __str__(self):
        return "Multipower: {}".format(self.value)

#the mainpower - used to power the transistors
_MAINPOWER = MultiPower(on = True)

class Transistor(Interface):
    """
    Transistor is the key component and simulates a single transistor
    """
    def __init__(self, connect_to_power = True):
        self._collector = Cathode(value_changed = self._update_state)
        self._base = Cathode(value_changed = self._update_state)
        self._emitter = Anode()

        #an output from the collector (an inverse of the emitter), used not NOT
        self._collector_output = Anode()

        if connect_to_power:
            _MAINPOWER.connect(self._collector)
            self._update_state()

        inputs = {}
        inputs["collector"] = self._collector
        inputs["base"] = self._base

        outputs = {}
        outputs["emitter"] = self.emitter
        outputs["collector output"] = self.collector_output

        super(Transistor, self).__init__(inputs, outputs)
        
    @property
    def collector(self):
        return self._collector

    @property
    def base(self):
        return self._base

    @property
    def emitter(self):
        return self._emitter

    @property
    def collector_output(self):
        return self._collector_output

    def _update_state(self):
        self._emitter.value = self._collector.value and self._base.value
        self._collector_output.value = self._collector.value and (not self._base.value)

    def __str__(self):
        return "Transistor: collector = {}, base = {}, emitter = {}, collector_output = {}".format(self._collector, self._base, self._emitter, self._collector_output)
