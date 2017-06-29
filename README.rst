=========================
Philbin Silicon Simulator
=========================

A work in progress...  

After watching `Crash Course Computer Science`_ I decided I wanted to make my own computer, after realising it would require a lot of transistors that I didn't have, I thought "hey, if I could code one transistor, I could use it many times".  

I have no idea what I was thinking!

The heart of PhilbinSS is a Transistor simulator and the components required to connect transistors together. These components are the only place where logic is coded, all other functions are created by connecting transistors together. 

Using these simple components you can create all the key elements of a computer - this is done through levels of abstraction:

* Transistor 
  
  * Not, And, Or 
  
    * Xor  
  
      * Half Adder
  
        * Full Adder
  
          * 8 bit Ripple Carry Adder
  
            * and so on...  

The current highest level of abstraction is ``8 bit ripple carry adder subtractor``.

The project is named after the host of the show `Carrie Anne Philbin`_.

Transistor
==========

A transistor has 3 connections (collector, base, emitter), when the collector and base are supplied with power, power is sent to the emitter (output). The transistor has a 2nd output connected to the collector, which will be powered when the collector is powered but the base is not.

You can create a transistor and connect it up using::

    # create the transistor and a power switch
    t = Transistor()
    p = Power()

    # connect the power to the transistor's base 
    p.connect(t.base)
    
    # the emitter will be False because the power to the base is off 
    print(t.emitter)
    # the output at the collector will be True
    print(t.collector_output)
    
    # turn the power on to the base
    p.on()

    # the emitter will be True
    print(t.emitter)
    # the output at the collector will be False
    print(t.collector_output)
    
By default, power is supplied to the transistor's collector, you can create an unpowered transistor using:: 

    t = Transistor(connect_to_power = False)

Using this simple construct you can create the key components of a computer.

Logic gates
===========

And
---

|andlogicgate|

An And gate is created using 2 transistors, the base connections are the inputs, the output from transistor 1's emitter is connected to transistor 2's collector and the result is the output of transistor 2's emitter::

    # create the transistors
    t1 = Transistor()
    t2 = Transistor(connect_to_power = False)

    # create the power switches 
    input_a = Power()
    input_b = Power()

    # connect the inputs 
    input_a.connect(t1.base)
    input_b.connect(t2.base)

    # connect t1's emitter to t2's collector
    t1.emitter.connect(t2.collector)

    # create a variable for the output
    output = t2.emitter

    # both inputs are off, the output is False
    input_a.off()
    input_b.off()
    print(output)

    # one input is on, the output is still False
    input_a.on()
    input_b.off()
    print(output)

    # both inputs are on, the output is True
    input_a.on()
    input_b.on()
    print(output)

Or
---

|orlogicgate|

An Or gate is created by connecting 2 transistors in parallel, the base connections are the inputs, the output is the obtained by joining the emitters::

    # create the transistors
    t1 = Transistor()
    t2 = Transistor()

    # create the power switches 
    input_a = Power()
    input_b = Power()

    # connect the inputs 
    input_a.connect(t1.base)
    input_b.connect(t2.base)

    # the output is the join of the 2 emitters.
    output = Join(t1.emitter, t2.emitter).output

    # both inputs are off, the output is False
    input_a.off()
    input_b.off()
    print(output)

    # input a is on, input b is off, the output is True
    input_a.on()
    input_b.off()
    print(output)

    # input a is off, input b is on, the output is True
    input_a.off()
    input_b.on()
    print(output)

    # both inputs are on, the output is True
    input_a.on()
    input_b.on()
    print(output)

`Martin O'Hanlon`_ `stuffaboutco.de`_ `@martinohanlon`_

 * images from `Crash Course Computer Science`_

.. _Martin O'Hanlon: https://github.com/martinohanlon
.. _stuffaboutco.de: http://stuffaboutco.de
.. _@martinohanlon: https://twitter.com/martinohanlon
.. _Crash Course Computer Science: https://www.youtube.com/watch?v=tpIctyqH29Q&list=PL8dPuuaLjXtNlUrzyH5r6jN9ulIgZBpdo
.. _Carrie Anne Philbin: https://twitter.com/MissPhilbin 

.. |andlogicgate| image:: docs/images/and.png
   :alt: and logic gate

.. |orlogicgate| image:: docs/images/or.png
   :alt: or logic gate
