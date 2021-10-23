import numpy as np

from StatsUtils.Stochastic import BrownionPathGen

class AmericanOption:
    
    def __init__(self, S_naught,Strike, Drift,Vol, BrownionMotionGen, Type = "Put", PayOffIndex = [] ):
        self.S_naught = S_naught
        self.Strike = Strike
        self.Drift = Drift
        self.Vol = Vol
        self.Type = Type
        self.BMPath = BrownionMotionGen.GeneratePaths()
        self.Maturity = BrownionMotionGen.Maturity
        self.NumPaths = BrownionMotionGen.NumPaths

        if( len(PayOffIndex)==0):
            self.PayoffIndex = [i for i in range( 1, self.Maturity+1)]
        self.GenerateRF()
        
    
    def GenerateRF(self):
        RFs = []
        for index in range(0,self.Maturity+1):
            RFs.append(self.GeometricBM(self.BMPath[index],index/365)) 
        self.RF_Path = RFs
    
    def GeometricBM( self, Section, Time ):
        return self.S_naught*np.e**( self.Vol*Section + ( self.Drift-(self.Vol**2 )/2)*Time )
    
    def RiskFactorPaths( self ):
        return np.array( self.RF_Path ).squeeze().T
    
    def GetImpliedPayOff( self, CrossSection ):
        if( self.Type=="Put" ):
            return np.maximum( self.Strike-CrossSection,0 )
        else:
            return np.maximum( CrossSection-self.Strike,0 )
        
    def DiscountFactor( self, CrossSectionIndex ):
        DF = self.DiscountCurve[:,CrossSectionIndex]
        return DF    
    
    def DiscountedRFPaths(self, IRModel ):
        RFPaths = self.RiskFactorPaths( )
        self.DiscountCurve = IRModel.GetDiscountCurve(self.NumPaths,self.Maturity)

        for index in range( self.Maturity,0,-1):
            DF = self.DiscountFactor(index)[:,np.newaxis]
            RFPaths[:,index-1:] = DF*RFPaths[:,index-1:]
            
        return RFPaths
         