import numpy as np
from numpy.core.fromnumeric import size

class BrownionPathGen:
    
    def __init__( self, Num_Paths, Maturity ):
        self.Num_Paths = Num_Paths 
        self.Maturity  = Maturity        #this is in days 
    
    #this is not optimal lets make a matrix of the std normal and then perform the operation to 
    #change its mean and std but for now lets leave it as it is
    def GenerateCrossSection( self, Last_Mean, DiffTime ):
        
        Normals = np.random.standard_normal( size=[self.Num_Paths,1] )
        
        Var = DiffTime/self.Maturity  # between two crosssection the time spend it difftime so var is also proportional to diff time
        
        Std = Var**0.5;
        
        # so basically the next cross-section will be data which was produced by last cross secion + 
        # std*RN . this can be proved to produce normal dist with mean given by last cross section and std .
        Adjusted_Normals = Std*Normals+Last_Mean 
        
        return Adjusted_Normals
    
    def GeneratePaths( self ):
        
        Path  = np.zeros([self.Num_Paths,1])
        
        Paths = [Path]
        for i in range( 0, self.Maturity ):
            Paths.append( self.GenerateCrossSection( Last_Mean = Paths[i], DiffTime = 1 ) ) #this difftime is for now 1 but we may change it in future to make it more advance 
        
        return Paths
    
            