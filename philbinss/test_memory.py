from components import Power
from memory import AndOrLatch, GatedLatch, EightBitRegister
from random import getrandbits

def test_andorlatch():
    latch = AndOrLatch()
    
    input_set = Power()
    input_reset = Power()

    input_set.connect(latch.set)
    input_reset.connect(latch.reset)

    assert not latch.set.value
    assert not latch.reset.value
    assert not latch.output.value

    input_set.on()
    assert latch.set.value
    assert not latch.reset.value
    assert latch.output.value
    
    input_set.off()
    assert not latch.set.value
    assert not latch.reset.value
    assert latch.output.value
    
    input_reset.on()
    assert not latch.set.value
    assert latch.reset.value
    assert not latch.output.value
    
    input_set.on()
    assert latch.set.value
    assert latch.reset.value
    assert not latch.output.value
    
    input_reset.off()
    assert latch.set.value
    assert not latch.reset.value
    assert latch.output.value

    input_set.off()
    assert not latch.set.value
    assert not latch.reset.value
    assert latch.output.value

def test_gatedlatch():
    latch = GatedLatch()

    input_data = Power()
    input_write = Power()

    input_data.connect(latch.data)
    input_write.connect(latch.write)

    assert not latch.data.value
    assert not latch.write.value
    assert not latch.output.value

    input_data.on()
    assert latch.data.value
    assert not latch.write.value
    assert not latch.output.value

    input_write.on()
    assert latch.data.value
    assert latch.write.value
    assert latch.output.value

    input_write.off()
    assert latch.data.value
    assert not latch.write.value
    assert latch.output.value

    input_data.off()
    assert not latch.data.value
    assert not latch.write.value
    assert latch.output.value

    input_write.on()
    assert not latch.data.value
    assert latch.write.value
    assert not latch.output.value

    input_write.off()
    assert not latch.data.value
    assert not latch.write.value
    assert not latch.output.value

def test_eightbitregister():
    reg = EightBitRegister()

    #create input power switches and connect up ripple carry adder
    inputs_data = []
    
    for i in range(8):
        input_bit = Power()
        
        input_bit.connect(reg.data.get_bit(i))
        
        inputs_data.append(input_bit)

    input_write = Power()
    input_write.connect(reg.write)
    
    #initial output should be 0
    last_write_value = 0
    assert reg.output.int_value == last_write_value 

    #do some random tests
    no_tests = 100
    for i in range(no_tests):
        #turn on random bits
        for input_data in inputs_data:
            if getrandbits(1) == 1:
                input_data.on()
            else:
                input_data.off()

        #write hasnt been enabled the output shouldnt have changed
        assert reg.output.int_value == last_write_value 

        #randomly turn on write enable
        if getrandbits(1) == 1:
            input_write.on()
            #if it was write enabled update the last write value
            last_write_value = reg.data.int_value
        else:
            input_write.off()
        
        #test to see if the output is still correct     
        assert reg.output.int_value == last_write_value

        input_write.off()

def run_tests():
    test_andorlatch()
    test_gatedlatch()    
    test_eightbitregister()

    print("memory - all tests run")

run_tests()
