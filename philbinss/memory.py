from components import Base
from logicgates import Or, Not, And
from mixins import SetResetInputMixin, OneOutputMixin

class AndOrLatch(Base, SetResetInputMixin, OneOutputMixin):
    def __init__():
        o = Or()
        a = And()
        n = Not()
        

    