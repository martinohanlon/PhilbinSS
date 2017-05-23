class Node(object):
    def __init__(self, value, value_changed):
        self._value_changed = value_changed
        self._value = value
        self._connection = None 

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(self, Cathode):
            raise TypeError("Cant set value of a cathode")

        self._update_value(value)

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, value):
        if value == None:
            self.disconnect()
        else:
            self.connect(value)

    def _update_value(self, value):
        if self._value != value:
            self._value = value
            if self._connection:
                self._connection._update_value(value)
            if self._value_changed:
                self._value_changed()

    def connect(self, cathode):
        if self._connection:
            raise Exception("node can only have 1 connection - use Split or Join")
        if isinstance(cathode, Anode):
            raise TypeError("cannot connect to a Anode")
        if not isinstance(cathode, Cathode):
            raise TypeError("can only connect to a Cathode")
        
        #update the connected cathodes value to this nodes value
        self._connection = cathode
        cathode._update_value(self._value)

    def disconnect(self):
        self._connection = None

    def __repr__(self):
        return "{}".format(self.value)

class Anode(Node):
    def __init__(self, value = False, value_changed = None):
        super(Anode, self).__init__(value, value_changed)

class Cathode(Node):
    def __init__(self, value_changed = None):
        super(Cathode, self).__init__(False, value_changed)
