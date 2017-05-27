from alu import HalfAdder, FullAdder, EightBitRippleCarryAdder
from components import Power
from random import randint

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

    in1.off()
    in2.off()
    in3.on()
    assert not fa.carry.value
    assert fa.sum.value

    in1.off()
    in2.on()
    in3.off()
    assert not fa.carry.value
    assert fa.sum.value

    in1.on()
    in2.on()
    in3.off()
    assert fa.carry.value 
    assert not fa.sum.value 

    in1.off()
    in2.on()
    in3.on()
    assert fa.carry.value 
    assert not fa.sum.value 

    in1.on()
    in2.off()
    in3.on()
    assert fa.carry.value 
    assert not fa.sum.value 

    in1.on()
    in2.on()
    in3.on()
    assert fa.carry.value 
    assert fa.sum.value 

def test_eightbitripplecarryadder():
    rca = EightBitRippleCarryAdder()

    #create input power switches and connect up ripple carry adder
    inputs_a = []
    inputs_b = []
    for i in range(8):
        input_a_bit = Power()
        input_b_bit = Power()
    
        input_a_bit.connect(rca.input_a.get_bit(i))
        input_b_bit.connect(rca.input_b.get_bit(i))
        
        inputs_a.append(input_a_bit)
        inputs_b.append(input_b_bit)

    no_tests = 50
    for i in range (no_tests):
        #turn on random bits
        for in_bit in inputs_a:
            in_bit.off()
            if randint(0,2) == 2:
                in_bit.on()
        
        for in_bit in inputs_b:
            in_bit.off()
            if randint(0,2) == 2:
                in_bit.on()

        #was there an overflow? if so was the result over 255
        if rca.carry.value:
            assert rca.input_a.int_value + rca.input_b.int_value > 255
        #if no overflow did it calculate correctly 
        if not rca.carry.value:
            assert rca.input_a.int_value + rca.input_b.int_value == rca.sum.int_value

def run_tests():
    test_halfadder()
    test_fulladder()
    test_eightbitripplecarryadder()

    print("alu - all tests run")

run_tests()