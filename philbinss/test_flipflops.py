from components import Power
from flipflops import SRFlipFlop

def test_srflipflop():
    p_set = Power()
    p_reset = Power()
    sr = SRFlipFlop()

    p_set.connect(sr.set)
    p_reset.connect(sr.reset)
    
    print(sr)

    p_set.on()

    print(sr)

    p_set.off()

    print(sr)

    p_reset.on()

    print(sr)



test_srflipflop()