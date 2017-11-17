from components import Power
from flipflops import SRFlipFlop, JKFlipFlop, DFlipFlop

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

def run_tests():
    test_srflipflop()
    test_jkflipflop()
    test_dflipflop()
    print("flipflops - all tests run")

run_tests()