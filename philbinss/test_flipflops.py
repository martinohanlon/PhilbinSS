from components import Power
from flipflops import SRFlipFlop, JKFlipFlop

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

def run_tests():
    test_srflipflop()
    test_jkflipflop()
    print("flipflops - all tests run")

run_tests()