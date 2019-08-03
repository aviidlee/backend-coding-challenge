from abc import abstractmethod

class ScoringMethod(object):
    '''
    classdocs
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
        
    