from components import Power
from flipflops import SRFlipFlop, JKFlipFlop, DFlipFlop, MasterSlaveJKFlipFlop, ThreeInputNand

def test_srflipflop():
    p_set = Power()
    p_reset = Power()
    sr = SRFlipFlop()

    p_set.connect(sr.set)
    p_reset.connect(sr.reset)
    
    assert sr.output_q_.value
    assert not sr.output_q.value
    
    p_set.on()

    assert not sr.output_q_.value
    assert sr.output_q.value
    
    p_set.off()

    assert not sr.output_q_.value
    assert sr.output_q.value
    
    p_reset.on()

    assert sr.output_q_.value
    assert not sr.output_q.value

    p_reset.off()

    assert sr.output_q_.value
    assert not sr.output_q.value

    #might as well test the 'illegal' state
    p_set.on()
    p_reset.on()

    assert not sr.output_q_.value
    assert not sr.output_q.value

def test_jkflipflop():
    p_j = Power()
    p_k = Power()
    p_clk = Power()
    jk = JKFlipFlop()

    p_j.connect(jk.input_j)
    p_k.connect(jk.input_k)
    p_clk.connect(jk.clock)

    assert jk.output_q_.value
    assert not jk.output_q.value

    p_j.on()
    assert jk.output_q_.value
    assert not jk.output_q.value

    p_clk.on()
    assert not jk.output_q_.value
    assert jk.output_q.value

    p_j.off()
    assert not jk.output_q_.value
    assert jk.output_q.value

    p_clk.off()
    assert not jk.output_q_.value
    assert jk.output_q.value

    p_k.on()
    assert not jk.output_q_.value
    assert jk.output_q.value

    p_clk.on()
    assert jk.output_q_.value
    assert not jk.output_q.value

    p_k.off()
    assert jk.output_q_.value
    assert not jk.output_q.value

    p_clk.off()
    assert jk.output_q_.value
    assert not jk.output_q.value


def test_threeinputnand():
    nand = ThreeInputNand()

    p_a = Power()
    p_b = Power()
    p_c = Power()

    p_a.connect(nand.input_a)
    p_b.connect(nand.input_b)
    p_c.connect(nand.input_c)

    assert nand.output.value

    p_a.on()

    assert nand.output.value

    p_b.on()

    assert nand.output.value 

    p_c.on()

    assert not nand.output.value

    p_a.off()

    assert nand.output.value


def test_msjkflipflop():
    p_j = Power()
    p_k = Power()
    p_clk = Power()
    msjk = MasterSlaveJKFlipFlop()

    p_j.connect(msjk.input_j)
    p_k.connect(msjk.input_k)
    p_clk.connect(msjk.clock)
    
    assert msjk.output_q.value
    assert not msjk.output_q_.value

    # RESET
    p_clk.on()
    p_k.on()

    # it should reset until the clock goes low
    assert msjk.output_q.value

    # did it reset
    p_clk.off()
    assert not msjk.output_q.value
    assert msjk.output_q_.value
    
    # make sure the value doesnt change when reset is turned off
    p_k.off()
    assert not msjk.output_q.value
    assert msjk.output_q_.value

    # or when the clock is back on
    p_clk.on()
    assert not msjk.output_q.value
    assert msjk.output_q_.value

    # SET
    p_j.on()

    # it shouldnt set until the clock goes low
    assert not msjk.output_q.value
    assert msjk.output_q_.value

    # did it set
    p_clk.off()
    assert msjk.output_q.value
    assert not msjk.output_q_.value

    # make sure the value doesnt change when set is turned off
    p_j.off()
    assert msjk.output_q.value
    assert not msjk.output_q_.value

    # or when the clock is back on
    p_clk.on()
    assert msjk.output_q.value
    assert not msjk.output_q_.value

    # RESET
    p_k.on()
    p_clk.off()
    assert not msjk.output_q.value
    assert msjk.output_q_.value

def test_dflipflop():
    p_d = Power()
    p_clk = Power()
    d = DFlipFlop()

    p_d.connect(d.input_d)
    p_clk.connect(d.clock)

    #clock is off, d is off
    assert not d.output_q.value
    assert d.output_q_.value

    p_clk.on()
    assert d.output_q.value
    assert not d.output_q_.value

    #turn d on, it should flip
    p_d.on()
    assert not d.output_q.value
    assert d.output_q_.value

    #turn d off, it should flip
    p_d.off()
    assert d.output_q.value
    assert not d.output_q_.value

    #turn d on, it should flip
    p_d.on()
    assert not d.output_q.value
    assert d.output_q_.value

    #turn clock off
    p_clk.off()
    assert not d.output_q.value
    assert d.output_q_.value
 
    #turning d on should do nothing
    p_d.on()
    assert not d.output_q.value
    assert d.output_q_.value
    
def print_debug(comps):
    for comp_key in comps.keys():
        print(comp_key + " - " + str(comps[comp_key]))

def run_tests():
    test_srflipflop()
    test_jkflipflop()
    test_dflipflop()
    test_threeinputnand()
    test_msjkflipflop()
    print("flipflops - all tests run")

run_tests()