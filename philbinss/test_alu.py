from alu import HalfAdder
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

def run_tests():
    test_halfadder()

    print("alu - all tests run")

run_tests()