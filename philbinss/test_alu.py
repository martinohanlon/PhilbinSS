from alu import HalfAdder, FullAdder
from components import Power

def test_halfadder():
    ha = HalfAdder()
    in1 = Power()
    in2 = Power()

    in1.connect(ha.input_a)
    in2.connect(ha.input_b)

    in1.off()
    in2.off()
    assert not ha.sum.value
    assert not ha.carry.value

    in1.on()
    in2.off()
    assert ha.sum.value
    assert not ha.carry.value

    in1.off()
    in2.on()
    assert ha.sum.value
    assert not ha.carry.value

    in1.on()
    in2.on()
    assert not ha.sum.value
    assert ha.carry.value    

def test_fulladder():
    fa = FullAdder()
    in1 = Power()
    in2 = Power()
    in3 = Power()

    in1.connect(fa.input_a)
    in2.connect(fa.input_b)
    in3.connect(fa.input_c)

    in1.off()
    in2.off()
    in3.off()
    assert not fa.carry.value
    assert not fa.sum.value

    in1.on()
    in2.off()
    in3.off()
    assert not fa.carry.value
    assert fa.sum.value

    in1.on()
    in2.on()
    in3.off()
    assert fa.carry.value 
    assert not fa.sum.value 

    in1.on()
    in2.on()
    in3.on()
    assert fa.carry.value 
    assert fa.sum.value 

def run_tests():
    test_halfadder()
    test_fulladder()

    print("alu - all tests run")

run_tests()