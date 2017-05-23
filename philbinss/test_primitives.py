from primitives import Node, Anode, Cathode
from threading import Event

def test_node():
    n = Node(False, None)

    assert not n.value
    n.value = True
    assert n.value 

    n = Node(True, None)

    assert n.value
    n.value = False
    assert not n.value 

def test_node_value_changed():
    def value_change():
        assert n.value

    n = Node(False, value_change)
    n.value = True

def test_anode():
    a = Anode(value = True)
    assert a.value

    a = Anode()
    assert not a.value
    
def test_anode_value_changed():
    event = Event()
    a = Anode(value_changed = event.set)
    
    a.value = True
    assert event.is_set

def test_cathode():
    c = Cathode()
    assert not c.value

def test_anode_cathode():
    a = Anode()
    c = Cathode()

    a.connect(c)
    a.value = True
    assert c.value

def test_cathode_value_changed():
    event = Event()
    a = Anode()
    c = Cathode(value_changed = event.set)
    a.connect(c)
    a.value = True
    assert event.is_set
    
def run_tests():
    test_node()
    test_node_value_changed()
    test_anode()
    test_anode_value_changed()
    test_cathode()
    test_anode_cathode()
    test_cathode_value_changed()
    

run_tests()
print("primitives - all tests run")