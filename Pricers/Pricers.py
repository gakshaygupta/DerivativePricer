import numpy as np

class AmericanMC:
    
    def __init__( self, Num_Basis, Regressor, Derivative, IRModel):

        self.Num_Basis = Num_Basis
        self.Regressor = Regressor
        self.Derivative = Derivative
        self.PayOffIndex = Derivative.PayoffIndex
        self.IRModel = IRModel
        self.RF_Paths = Derivative.RiskFactorPaths()
        self.NumPaths,self.Maturity = self.RF_Paths.shape
        self.DiscountCurve = IRModel.GetDiscountCurve(self.NumPaths,self.Maturity) #this discount curve will be between two corssecgtion 
        self.StoppingRule = np.zeros([self.NumPaths,self.Maturity])
        self.StoppingRule[:,self.Maturity] = np.ones_like( self.StoppingRule[:,self.Maturity] )
        self.PayOffMatrix = np.zeros_like(self.StopingRule)
        self.RegCoeffs = []
        
    def GenerateNPV( self ):
        #generate implied value payoff matrix
        Implied_Value = []
        for index in self.PayOffIndex:
            CorssSection = self.GetCrossSection(index)
            Implied_Value.append( self.Derivative.GetImpliedPayOff( CorssSection ) )
        
        Implied_Value = np.array(Implied_Value)

        #do AMC Here
        Discounted_IV = Implied_Value
        for index in self.PayOffIndex[:,-1]:
            Discounted_IV[:,index:] = self.DiscountFactor(index)*Discounted_IV[:,index:]
            if index == self.PayOffIndex[-1]:
                continue
            
            CF = self.GetCashFlow(Discounted_IV)
            X  = self.RF_Paths[:,index]
            self.PerformRegression(CF,X)
            E_DCF = self.GetCondCF(X)
            
            Stopping = Implied_Value[:,index]>=E_DCF
            
            self.UpdateStopingRule(Stopping)
            
        self.Discounted_IV = Discounted_IV
        #TBD
    def GetValue(self):
        Value = 0
        for index in range( 0, self.NumPaths ):
            Value += self.Discounted_IV[index,self.StoppingRule[index]]
        return Value
    
    def PerformRegression( self, Y,X ):
        self.RegCoeff = np.polyfit(X,Y,self.Num_Basis)
        self.RegCoeffs.append( self.RegCoeffs )
    
    def GetCondCF( self,X):
        P = np.poly1d(X)
        return P(X)
    
    def GetCashFlow(self, Discounted_IV ):
        CF = np.zeros([self.NumPaths,1])
        for i in range(0, self.NumPaths):
            CF[i] = Discounted_IV[i,self.StopingRule[i]]
        return CF
    
    def GetCrossSection( self, CorssSectionIndex ):
        return self.RF_Paths[:,CorssSectionIndex]
    
    def UpdateStopingRule( self, Stopping):
        for index in range(0,self.NumPaths):
            if( Stopping[index]!=0 ): 
                continue
            self.StoppingRule[index] = Stopping[index]        
            
    def DiscountFactor( self, CrossSectionIndex ):
        DF = self.DiscountCurve[:,CrossSectionIndex]
        return DF

    def DiscountCrossSection( self, CrossSectionIndex ):
        #not using this currently
        CrossSection_RF = self.RF_Paths[:,CrossSectionIndex]
        CrossSection_DCS = self.DiscountCurve[:,CrossSectionIndex]
        
        return CrossSection_RF*CrossSection_DCS