from components import Power
from multiplexers import TwoToOneMultiplexer, FourToOneMultiplexer, TwoToFourDecoder

def test_twotoonemultiplexer():
    mp = TwoToOneMultiplexer()

    in1 = Power()
    in2 = Power()
    sig = Power()

    in1.connect(mp.input_a)
    in2.connect(mp.input_b)
    sig.connect(mp.signal)

    #when the signal is off, output is a, when signal is on output is b
    
    assert not mp.output.value

    in1.on()
    assert mp.output.value

    sig.on()
    assert not mp.output.value
    in2.on()
    assert mp.output.value

    sig.off()
    assert mp.output.value
    in1.off()
    assert not mp.output.value

    sig.on()
    assert mp.output.value
    in2.off()
    assert not mp.output.value

def test_fourtoonemultiplexer():
    mp = FourToOneMultiplexer()

    in1 = Power()
    in2 = Power()
    in3 = Power()
    in4 = Power()

    sig1 = Power()
    sig2 = Power()

    in1.connect(mp.input_a)
    in2.connect(mp.input_b)
    in3.connect(mp.input_c)
    in4.connect(mp.input_d)

    sig1.connect(mp.signal_a)
    sig2.connect(mp.signal_b)

    assert not mp.output.value

    in1.on()
    assert mp.output.value

    sig1.on()
    assert not mp.output.value

    in2.on()
    assert mp.output.value

    sig2.on()
    assert not mp.output.value

    in4.on()
    assert mp.output.value
    
    sig1.off()
    assert not mp.output.value

    in3.on()
    assert mp.output.value
    
    in3.off()
    assert not mp.output.value

def test_twotofourdecoder():
    dc = TwoToFourDecoder()

    in1 = Power()
    in2 = Power()

    in1.connect(dc.input_a)
    in2.connect(dc.input_b)
    assert dc.output_a.value
    assert not dc.output_b.value
    assert not dc.output_c.value
    assert not dc.output_d.value

    in1.on()
    assert not dc.output_a.value
    assert dc.output_b.value
    assert not dc.output_c.value
    assert not dc.output_d.value

    in1.off()
    in2.on()
    assert not dc.output_a.value
    assert not dc.output_b.value
    assert dc.output_c.value
    assert not dc.output_d.value

    in1.on()
    in2.on()
    assert not dc.output_a.value
    assert not dc.output_b.value
    assert not dc.output_c.value
    assert dc.output_d.value
    
def run_tests():
    test_twotoonemultiplexer()
    test_fourtoonemultiplexer()
    test_twotofourdecoder()

run_tests()
print("multiplexers - all tests run")