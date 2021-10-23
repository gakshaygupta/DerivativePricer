import numpy as np
from numpy.core.fromnumeric import size


class BrownionPathGen:

    def __init__(self, NumPaths, Maturity):
        self.NumPaths = NumPaths
        self.Maturity = Maturity  # this is in days

    # this is not optimal lets make a matrix of the std normal and then perform the operation to
    # change its mean and std but for now lets leave it as it is
    def GenerateCrossSection(self, Last_Mean, DiffTime):

        Normals = np.random.standard_normal(size=[self.NumPaths, 1])

        # have to adjust for leap year
        # between two crosssection the time spend it difftime so var is also proportional to diff time
        Var = DiffTime/365

        Std = Var**0.5

        # so basically the next cross-section will be data which was produced by last cross secion +
        # std*RN . this can be proved to produce normal dist with mean given by last cross section and std .
        Adjusted_Normals = Std*Normals+Last_Mean

        return Adjusted_Normals

    def GeneratePaths(self):

        Path = np.zeros([self.NumPaths, 1])

        Paths = [Path]
        # lets find out a matrix operation to do this . will be much faster
        # Maturity is a number for now but should be a date which should be compared to the global date
        for i in range(0, self.Maturity - 1):
            # this difftime is for now 1 but we may change it in future to make it more advance
            Paths.append(self.GenerateCrossSection(
                Last_Mean=Paths[i], DiffTime=1))

        return Paths
