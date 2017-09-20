import itertools
from components import Power
from memory import AndOrLatch, GatedLatch, EightBitRegister, RAMCell, SixteenBitMemory, SixteenByteMemory
from random import getrandbits

def test_andorlatch():
    latch = AndOrLatch()
    _str = latch.__str__()
    
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
    _str = latch.__str__()

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
    _str = reg.__str__()

    #create input power switches and connect up the register
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

def test_ramcell():
    rc = RAMCell()
    _str = rc.__str__()
    
    in_col = Power()
    in_row = Power()
    in_we = Power()
    in_re = Power()
    in_data = Power()

    in_col.connect(rc.col)
    in_row.connect(rc.row)
    in_we.connect(rc.write_enable)
    in_re.connect(rc.read_enable)
    in_data.connect(rc.data_in)

    assert not rc.col.value 
    assert not rc.row.value 
    assert not rc.write_enable.value 
    assert not rc.read_enable.value 
    assert not rc.data_in.value 
    assert not rc.data_out.value 
    
    #data can only be written if the col, row are on
    in_we.on()
    in_data.on()
    assert not rc.col.value 
    assert not rc.row.value 
    assert rc.write_enable.value 
    assert not rc.read_enable.value 
    assert rc.data_in.value 
    assert not rc.data_out.value 
    in_we.off()
    in_re.on()
    assert not rc.col.value 
    assert not rc.row.value 
    assert not rc.write_enable.value 
    assert rc.read_enable.value 
    assert rc.data_in.value 
    assert not rc.data_out.value 
    in_re.off()
    in_data.off()
    assert not rc.col.value 
    assert not rc.row.value 
    assert not rc.write_enable.value 
    assert not rc.read_enable.value 
    assert not rc.data_in.value 
    assert not rc.data_out.value 
    
    #write data to 1
    in_col.on()
    in_row.on()
    in_we.on()
    in_data.on()
    assert rc.col.value 
    assert rc.row.value 
    assert rc.write_enable.value 
    assert not rc.read_enable.value 
    assert rc.data_in.value 
    assert not rc.data_out.value 

    #read data
    in_we.off()
    in_data.off()
    in_re.on()
    assert rc.col.value 
    assert rc.row.value 
    assert not rc.write_enable.value 
    assert rc.read_enable.value 
    assert not rc.data_in.value 
    assert rc.data_out.value 
    in_re.off()

    #write data to 0
    in_we.on()
    in_data.off()
    assert rc.col.value 
    assert rc.row.value 
    assert rc.write_enable.value 
    assert not rc.read_enable.value 
    assert not rc.data_in.value 
    assert not rc.data_out.value 
    
    #read data
    in_we.off()
    in_data.off()
    in_re.on()
    assert rc.col.value 
    assert rc.row.value 
    assert not rc.write_enable.value 
    assert rc.read_enable.value 
    assert not rc.data_in.value 
    assert not rc.data_out.value 

    #turn it all off
    in_re.off()
    in_col.off()
    in_row.off()
    assert not rc.col.value 
    assert not rc.row.value 
    assert not rc.write_enable.value 
    assert not rc.read_enable.value 
    assert not rc.data_in.value 
    assert not rc.data_out.value 

def get_binary_states(no_inputs):
    return list(itertools.product(*[(False, True)] * no_inputs))

def test_sixteenbitmemory():
    mem = SixteenBitMemory()
    
    # create input power switches and connect up 
    inputs_address = []
    for i in range(4):
        input_bit = Power()
        input_bit.connect(mem.address.get_bit(i))
        inputs_address.append(input_bit)

    input_data = Power()
    input_data.connect(mem.data_in)
    input_write = Power()
    input_write.connect(mem.write_enable)
    input_read = Power()
    input_read.connect(mem.read_enable)

    # test that you can only read and write when enabled

    # test - its not written
    input_data.on()
    assert not mem.data_out.value

    # write a value
    input_write.on()
    input_write.off()

    # test - its not being read
    assert not mem.data_out.value

    # test - that it can be read
    input_read.on()
    assert mem.data_out.value

    input_read.off()
    input_data.off()

    # get all possible addresses
    addresses = get_binary_states(4)

    #write random values to memory addresses
    test_values = []
    for address in addresses:
        inputs_address[0].value = address[0]        
        inputs_address[1].value = address[1]
        inputs_address[2].value = address[2]
        inputs_address[3].value = address[3]
        test_value = bool(getrandbits(1))
        input_write.on()
        input_data.value = test_value
        input_write.off()
        test_values.append(test_value)

    input_data.off()

    #read values from memory and check they match
    a = 0
    for address in addresses:
        inputs_address[0].value = address[0]        
        inputs_address[1].value = address[1]
        inputs_address[2].value = address[2]
        inputs_address[3].value = address[3]
        input_read.on()
        assert mem.data_out.value == test_values[a]
        input_read.off()
        a += 1

def get_eight_bit_switch(eight_bit_input):
    switches = []

    for i in range(8):
        power_bit = Power()
        power_bit.connect(eight_bit_input.get_bit(i))        
        switches.append(power_bit)

    return switches

def test_sixteenbytememory():
    mem = SixteenByteMemory()

    # create input power switches and connect up 
    inputs_address = []
    for i in range(4):
        input_bit = Power()
        input_bit.connect(mem.address.get_bit(i))
        inputs_address.append(input_bit)

    inputs_data = get_eight_bit_switch(mem.data_in)

    input_write = Power()
    input_write.connect(mem.write_enable)

    input_read = Power()
    input_read.connect(mem.read_enable)

    # test that you can only read and write when enabled

    # test - its not written
    inputs_data[0].on()
    assert mem.data_out.int_value == 0

    # write a value
    input_write.on()
    input_write.off()

    # test - its not being read
    assert mem.data_out.int_value == 0
    
    # test - that it can be read
    input_read.on()
    assert mem.data_out.int_value == 1

    input_read.off()
    inputs_data[0].off()

def run_tests():
    test_andorlatch()
    test_gatedlatch()    
    test_eightbitregister()
    test_ramcell()
    test_sixteenbitmemory()
    test_sixteenbytememory()

    print("memory - all tests run")

run_tests()
