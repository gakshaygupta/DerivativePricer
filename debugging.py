# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from StatsUtils.Stochastic import BrownionPathGen
from Derivatives.Options import AmericanOption
from IRModels.DeterministciModels import ConstIR
from Pricers.Pricers import AmericanMC
import numpy as np


# %%
NumPaths = 5000
Maturity = 1000
Strike = 100
S_naught = 90
Vol = 0.2
Drift=R=7/100


# %%
BM = BrownionPathGen(NumPaths,Maturity)
Option = AmericanOption(S_naught, Strike,Drift,Vol,BM)
IRModel = ConstIR(R)
Pricer = AmericanMC(3,"linear",Option,IRModel)


# %%
#value = Pricer.GetValue()


# %%



# %%



# %%
paths = Option.DiscountedRFPaths(IRModel)
import matplotlib.pyplot as plt
plt.plot( np.average(paths.T, axis =  1 )) 


# %%



