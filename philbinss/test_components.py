from primitives import Anode, Cathode
from components import Transistor, Split, Join, Power, MultiPower

def test_transistor():
    t = Transistor(connect_to_power = False)
    p = Power()
    sw = Power()
    p.connect(t.collector)
    sw.connect(t.base)
    
    p.off()
    sw.off()
    assert not t.collector.value
    assert not t.collector_output.value
    assert not t.base.value
    assert not t.emitter.value
    p.on()
    assert t.collector.value
    assert t.collector_output.value
    assert not t.base.value
    assert not t.emitter.value
    sw.on()
    assert t.collector.value
    assert not t.collector_output.value
    assert t.base.value
    assert t.emitter.value
    sw.off()
    assert t.collector.value
    assert t.collector_output.value
    assert not t.base.value
    assert not t.emitter.value
    p.off()
    assert not t.collector.value
    assert not t.collector_output.value
    assert not t.base.value
    assert not t.emitter.value

def test_powered_transistor():
    t = Transistor()
    assert t.collector.value
    
def test_split():
    sw = Power()
    c1 = Cathode()
    c2 = Cathode()
    c3 = Cathode()
    split = Split(c1, c2)
    sw.connect(split.input)

    sw.off()
    assert not split.input.value
    assert not c1.value
    assert not c2.value
    sw.on()
    assert split.input.value
    assert c1.value
    assert c2.value
    split.connect(c3)
    assert c3.value
    sw.off()
    assert not split.input.value
    assert not c1.value
    assert not c2.value
    assert not c3.value

def test_join():
    sw1 = Power()
    sw2 = Power()
    sw3 = Power()
    o = Cathode()
    
    j = Join(sw1, sw2)
    j.output.connect(o)
    
    sw1.off()
    sw2.off()
    sw3.off()
    assert not j.value
    assert not o.value

    sw1.on()
    assert j.value
    assert o.value
    sw2.on()
    assert j.value
    assert o.value
    
    sw1.off()
    sw2.off()
    assert not j.value
    assert not o.value

    sw3.on()
    j.connect(sw3)
    assert j.value
    assert o.value
    
    sw1.off()
    sw2.off()
    sw3.off()
    assert not j.value
    assert not o.value

def test_power():
    p = Power()
    assert not p.value
    p.on()
    assert p.value
    p.off()
    assert not p.value
    
    p = Power(on = True)
    assert p.value

def test_multipower():
    mp = MultiPower()
    c1 = Cathode()
    c2 = Cathode() 
    
    mp.connect(c1)
    assert not c1.value
    mp.on()
    assert c1.value
    
    mp.connect(c2)
    assert c2.value

    mp.off()
    assert not c1.value
    assert not c2.value

    mp = MultiPower(on = True)
    mp.connect(c1)
    assert c1.value
    
def run_tests():
    test_power()
    test_multipower()
    test_transistor()
    test_powered_transistor()
    test_split()
    test_join()

    print("components - all tests run")

run_tests()
