import numpy as np

class AmericanMC:
    
    def __init__( self, Num_Basis, Regressor, Derivative, IRModel):

        self.Num_Basis = Num_Basis #This variable defines the number of basis that should be used for regression
        self.Regressor = Regressor #this variable defines which regression to use ( currently the regression is linear)
        self.Derivative = Derivative #This the derivative we want to price 
        self.PayOffIndex = Derivative.PayoffIndex #this index tells us which indexes to be used for calculating the value 
        self.IRModel = IRModel # this is interest rate model . this can be stochastic or deterministic 
        self.RF_Paths = Derivative.RiskFactorPaths() # this variabl carries the riskfactor paths
        self.NumPaths,self.Maturity = self.RF_Paths.shape
        self.DiscountCurve = IRModel.GetDiscountCurve(self.NumPaths,self.Maturity+1) #this discount curve will be between two corssecgtion 
        self.StoppingRule = [self.Maturity-2]*self.NumPaths # this matrix defines the stoping rule for pricing
        self.PayOffMatrix = np.zeros_like(self.StoppingRule) # this matrix gives the payoff for each crossection
        self.RegCoeffs = [] #ths array stores the reg coefficients 
        
    def GenerateNPV( self ):
        #generate implied value payoff matrix
        Implied_Value = []
        for index in self.PayOffIndex:
            CorssSection = self.GetCrossSection(index)
            Implied_Value.append( self.Derivative.GetImpliedPayOff( CorssSection ) )
        
        Implied_Value = np.array(Implied_Value).T

        #do AMC Here
        Discounted_IV = Implied_Value
        for index in self.PayOffIndex[::-1]:
            DF = self.DiscountFactor(index)[:,np.newaxis]
    
            Discounted_IV[:,index-1:] = DF*Discounted_IV[:,index-1:]
            
            CF = self.GetCashFlow(Discounted_IV)
            X  = self.RF_Paths[:,index]
            self.PerformRegression(CF,X)
            E_DCF = self.GetCondCF(X)
            
            Stopping = Implied_Value[:,index-1]>=E_DCF
            
            self.UpdateStopingRule(Stopping, index)
            
        self.Discounted_IV = Discounted_IV
        
    def GetValue(self):
        self.GenerateNPV()
        Value = 0
        for index in range( 0, self.NumPaths ):
            Value += self.Discounted_IV[index,self.StoppingRule[index]]
        return Value
    
    def PerformRegression( self, Y,X ):
        self.RegCoeff = np.polyfit(X,Y,self.Num_Basis)
        self.RegCoeffs.append( self.RegCoeff )
    
    def GetCondCF( self,X):
        P = np.poly1d(self.RegCoeff)
        return P(X)
    
    def GetCashFlow(self, Discounted_IV ):
        CF = np.zeros([self.NumPaths])
        for i in range(0, self.NumPaths):
            CF[i] = Discounted_IV[i][self.StoppingRule[i]]
        return CF
    
    def GetCrossSection( self, CorssSectionIndex ):
        return self.RF_Paths[:,CorssSectionIndex]
    
    def UpdateStopingRule( self, Stopping, StopIndex):
        for index in range(0,self.Maturity):
            if( not Stopping[index] ):
                continue
            self.StoppingRule[index] = StopIndex
            
    def DiscountFactor( self, CrossSectionIndex ):
        DF = self.DiscountCurve[:,CrossSectionIndex]
        return DF

    def DiscountCrossSection( self, CrossSectionIndex ):
        #not using this currently
        CrossSection_RF = self.RF_Paths[:,CrossSectionIndex]
        CrossSection_DCS = self.DiscountCurve[:,CrossSectionIndex]
        
        return CrossSection_RF*CrossSection_DCS