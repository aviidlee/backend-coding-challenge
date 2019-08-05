from abc import abstractmethod

class ScoringMethod(object):
    '''
    Abstract base class for a scoring method and its associated parameters. 
    
    Given two strings, return a number in range [0, 1] representing how closely
    the strings match, where the higher the number, the closer the match. 

    Methods:
        score -- returns a score between 0 and 1 inclusive, indicating how closely  
                 two strings match
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    @abstractmethod
    def score(self, query, text):
        '''Text-based only match score between query and text.
        
        Returns: 
            A score in range [0, 1] where 1 indicates the best possible match
            between query and text, and 0 indicates no match.
        '''
        pass
    
    @abstractmethod
    def name(self):
        '''Returns name of this scoring algorithm. 
        '''
        
    
