import numpy as np


class ConstIR:
    def __init__(self, R):
        self.R = R

    def GetDiscountCurve(self, NumPaths, Maturity):
        DF = np.ones([NumPaths, Maturity])/365
        DF = np.e**(-self.R*DF)
        return DF
