class Node(object):
    """
    A node is the lowest level component and represents a single binary state. 
    
    A node can be connected to another node, when its value changes so does the value of its connected node.
    """
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

    def __str__(self):
        return "{}".format(self.value)

class Anode(Node):
    """
    An Anode is a type of node which emits a value (like an Anode which emits electrons!). 
    
    An Anode cannot be connected to, but an anode can connect to other nodes. 
    """
    def __init__(self, value = False, value_changed = None):
        super(Anode, self).__init__(value, value_changed)

class Cathode(Node):
    """
    A Cathode is a type of node which receives a value (like a Cathode which received electrons!).abs

    A Cathode's value cannot be changed directly, it can only be changed by a node which connects to it.
    """
    def __init__(self, value_changed = None):
        super(Cathode, self).__init__(False, value_changed)
