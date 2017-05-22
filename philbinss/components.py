from primitives import Anode, Cathode

class Split():
    """
    A Split is used to split 1 input into many outputs
    """
    def __init__(self, *outputs):
        #if the input changes, update the outputs
        self._input = Cathode(value_changed = self._update_state)
        self._outputs = []
        for output in outputs:
            self.connect(output)

    @property
    def input(self):
        return self._input

    def connect(self, output):
        #output must be a cathode
        if isinstance(output, Anode):
            raise TypeError("cannot output to a Anode")
        if not isinstance(output, Cathode):
            raise TypeError("output must be a Cathode")
        
        #create an anode which will connect to the output
        anode = Anode()
        anode.connect(output)
        self._outputs.append(anode)

        self._update_state()
        
    def _update_state(self):
        for output in self._outputs:
            output.value = self.value

    @property
    def value(self):
        return self._input.value

    def __repr__(self):
        return str(self.input)

class Join():
    """
    A join is used to bring multiple inputs into 1 output
    """
    def __init__(self, *inputs):
        self._output = Anode()
        self._inputs = []
        for aninput in inputs:
            self.connect(aninput)
    
    @property
    def output(self):
        return self._output

    def connect(self, aninput):
        if not isinstance(aninput, Cathode) and not isinstance(aninput, Anode):
            raise TypeError("input must be an Anode or Cathode")

        #add the input to the connections
        self._inputs.append(aninput)
        
        #create and connect cathode to the input
        cathode = Cathode(value_changed = self._update_state)
        aninput.connect(cathode)

        self._update_state()
            
    def _update_state(self):
        self.output.value = self.value
        
    @property
    def value(self):
        #if any node is True, return True, else False
        for aninput in self._inputs:
            if aninput.value:
                return True
        return False

    def __repr__(self):
        return "{}".format(self.value)

class Power(Split):
    """
    A Power is a Split connected up to Anode, it can acceptable multiple connections 
    and can be turned on and off.
    """
    def __init__(self, on = False):
        super(Power, self).__init__()

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

#the mainpower - used to power the transistors
_MAINPOWER = Power(on = True)

class Transistor():
    def __init__(self, connect_to_power = True):
        self.collector = Cathode(value_changed = self._update_state)
        self.base = Cathode(value_changed = self._update_state)
        self.emitter = Anode()

        #an output from the collector (an inverse of the emitter), used not NOT
        self.collector_output = Anode()

        if connect_to_power:
            _MAINPOWER.connect(self.collector)
        
        self._update_state()

    def _update_state(self):
        self.emitter.value = self.collector.value and self.base.value
        self.collector_output.value = self.collector.value and (not self.base.value)

    def __repr__(self):
        return "{},{},{}".format(self.collector, self.base, self.emitter)

    def __str__(self):
        return "collector = {}, base = {}, emitter = {}, collector_output = {}".format(self.collector, self.base, self.emitter, self.collector_output)

if __name__ == "__main__split":

    sw1 = Power()
    c1 = Cathode()
    c2 = Cathode()
    split = Split(c1, c2)
    sw1.connect(split.input)
    #sw1.connect(Split(c1, c2).input)
    print("{} {}".format(c1, c2))
    sw1.on()
    print("{} {}".format(c1, c2))
    sw1.off()
    print("{} {}".format(c1, c2))
    

if __name__ == "__main__join":

    sw1 = Power()
    sw2 = Power()
    sw3 = Power()
    sw1.on()
    sw2.on()
    sw3.on()
    o = Cathode()
    #join = Join(sw1, sw2)
    #join.connect(sw3)
    #join.output.connect(o)
    Join(sw1, sw2, sw3).output.connect(o)
    print(o)
    sw1.off()
    print(o)
    sw1.off()
    sw2.off()
    sw3.off()
    print(o)
    
if __name__ == "__main__":

    t1 = Transistor()
    t2 = Transistor(connect_to_power = False)
    sw1 = Power()
    sw2 = Power()
    sw1.connect(t1.base)
    sw2.connect(t2.base)
    t1.emitter.connect(t2.collector)
    sw1.on()
    sw2.on()
    print(t1)
    print(t2)