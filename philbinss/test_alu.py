from alu import HalfAdder, FullAdder, EightBitRippleCarryAdder, EightBitRippleCarryAdderSubtractor, ALU
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

def get_eight_bit_switch(eight_bit_input):
    switches = []

    for i in range(8):
        power_bit = Power()
        power_bit.connect(eight_bit_input.get_bit(i))        
        switches.append(power_bit)

    return switches

def test_eightbitripplecarryadder():
    rca = EightBitRippleCarryAdder()

    #create input power switches and connect up ripple carry adder
    inputs_a = get_eight_bit_switch(rca.input_a)
    inputs_b = get_eight_bit_switch(rca.input_b)

    #do some random tests
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

def test_eightbitripplecarryaddersubtractor():
    rcas = EightBitRippleCarryAdderSubtractor()

    #create input power switches and connect up ripple carry adder
    inputs_a = get_eight_bit_switch(rcas.input_a)
    inputs_b = get_eight_bit_switch(rcas.input_b)

    op = Power()
    op.connect(rcas.operator)

    #do some random tests
    no_tests = 100
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

        #random op
        op.off()
        if randint(0,1) == 1:
            op.on()

        #subtract
        if op.value:
            #if no overflow did it calculate correctly 
            if rcas.carry.value:
                assert rcas.input_a.int_value - rcas.input_b.int_value == rcas.sum.int_value
            #was there an overflow? if so was the result less than 0
            if not rcas.carry.value:
                assert rcas.input_a.int_value - rcas.input_b.int_value < 0

        #addition
        else:
            #was there an overflow? if so was the result over 255
            if rcas.carry.value:
                assert rcas.input_a.int_value + rcas.input_b.int_value > 255
            #if no overflow did it calculate correctly 
            if not rcas.carry.value:
                assert rcas.input_a.int_value + rcas.input_b.int_value == rcas.sum.int_value

def test_alu():
    alu = ALU()

    #create input power switches and connect up ripple carry adder
    inputs_a = get_eight_bit_switch(alu.input_a)
    inputs_b = get_eight_bit_switch(alu.input_b)

    op = Power()
    op.connect(alu.operator)

    #do some random tests
    no_tests = 100
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

        #random op
        op.off()
        if randint(0,1) == 1:
            op.on()

        #subtract
        if op.value:
            #if no overflow did it calculate correctly 
            if alu.carry.value:
                assert alu.input_a.int_value - alu.input_b.int_value == alu.sum.int_value
                assert not alu.overflow.value
                assert not alu.negative.value
            #was there an overflow? if so was the result less than 0
            if not alu.carry.value:
                assert alu.input_a.int_value - alu.input_b.int_value < 0
                assert alu.overflow.value
                assert alu.negative.value
        #addition
        else:
            #was there an overflow? if so was the result over 255
            if alu.carry.value:
                assert alu.input_a.int_value + alu.input_b.int_value > 255
                assert alu.overflow.value
                assert not alu.negative.value
            #if no overflow did it calculate correctly 
            if not alu.carry.value:
                assert alu.input_a.int_value + alu.input_b.int_value == alu.sum.int_value
                assert not alu.overflow.value
                assert not alu.negative.value
                
def run_tests():
    test_halfadder()
    test_fulladder()
    test_eightbitripplecarryadder()
    test_eightbitripplecarryaddersubtractor()
    test_alu()

    print("alu - all tests run")

run_tests()
