from tools.scoringmethods.scoringmethod import ScoringMethod
from pyjarowinkler import distance

class JaroWinkler(ScoringMethod):
    '''
    Computes match between two strings using the Jaro-Winkler algorithm. 
    
    Attributes: 
        winkler -- whether or not to use Winkler's modification to Jaro's 
                   algorithm, which weights prefix matches more highly.
        winkler_adj -- same as winkler... author of pyjarowinkler seems to have 
                       duplicate arguments. 
        scaling -- scale factor for Winkler adjustment. 

    '''


    def __init__(self, winkler=True, winkler_adj=True, scaling=0.1):
        self.winkler = winkler 
        self.winkler_adj = winkler_adj
        self.scaling = scaling 
    
    
    def score(self, query, matchString):
        '''Returns the Jaro-Winkler distance between query and matchString.'''
        if(len(query) == 0 or len(matchString) == 0):
            return 0.0
        
        return distance.get_jaro_distance(query, matchString, winkler=self.winkler,
                                          winkler_ajustment=self.winkler_adj, 
                                          scaling=self.scaling)
    
    
    def name(self):
        return 'Jaro-Winkler'
