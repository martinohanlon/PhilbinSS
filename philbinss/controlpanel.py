from guizero import App, CheckBox, Text, Combo, Box
from logicgates import Not, And, Or, Xor
from components import Power
from alu import HalfAdder, FullAdder, EightBitRippleCarryAdder

class ControlPanel():
    def __init__(self):
        self.components = {"AND": And, "OR": Or, "XOR": Xor, "NOT": Not, "Half Adder": HalfAdder, "Full Adder": FullAdder}

        self.app = App(title = "Philbin Silicon Simulator", layout = "grid")
        self.box_component = Box(self.app, grid = [0,1])
        
        self.combo = Combo(self.box_component, options = list(self.components.keys()), command = self.reload_component)

        self.setup_component()

        self.app.display()

    def setup_component(self):
        #create the component
        self.component = self.components[self.combo.get()]()
        self.box_inputs = Box(self.app, layout = "grid", grid = [0,0])
        self.box_outputs = Box(self.app, layout = "grid", grid = [0,2])
        
        self.input_power = []
        self.input_checks = []
        self.output_checks = []

        #setup the inputs and power switches
        #for i in range(len(self.component.inputs)):
        i = 0
        for input_key in self.component.inputs:
            p = Power()
            p.connect(self.component.inputs[input_key])
            self.input_power.append(p)
            self.input_checks.append(CheckBox(self.box_inputs, text = input_key, grid=[i,0], command=self.update_values))
            i += 1

        #setup the outputs
        o = 0
        for output_key in self.component.outputs:
            output_check = CheckBox(self.box_outputs, text = output_key, grid=[o,2])
            output_check.configure(state = "disabled")
            self.output_checks.append(output_check)
            o += 1

        self.update_values()

    def update_values(self):
        #set the power switched based on the check boxes
        for i in range(len(self.input_checks)):
            self.input_power[i].value = (self.input_checks[i].get_value() == 1) 

        #update the outputs
        #for o in range(len(self.component.outputs)):
        o = 0
        for output_key in self.component.outputs:
            if self.component.outputs[output_key].value:
                self.output_checks[o].select()
            else:
                self.output_checks[o].deselect()
            o += 1

    def reload_component(self,x):
        self.box_inputs.destroy()
        self.box_outputs.destroy()
        self.setup_component()
        self.app.display()

cp = ControlPanel()

