from repairs.backend.algorithm import *

class fd:
    def __init__(self, attributes, lhs, rhs):
        self.rhs_str = rhs
        self.lhs_str = lhs
        
        self.lhs = { attributes.index(a) for a in lhs }
        self.rhs = { attributes.index(a) for a in rhs }
        
        print(self.lhs)
        
    def satisfied(self, tx, ty):
        
        tx_lhs = project(tx, self.lhs)
        tx_rhs = project(tx, self.rhs)
        
        ty_lhs = project(ty, self.lhs)
        ty_rhs = project(ty, self.rhs)
        
        if tx_lhs == ty_lhs and tx_rhs != ty_rhs:
            return False
        else:
            return True