import numpy as np

class ConstIR:
    def __init__( self, R ):
        self.R = R
    
    def GetDiscountCurve( self, NumPaths, Maturity ):
        DF = np.ones([NumPaths,Maturity+1])
        DF = DF/(1+self.R)
        return DF
    