'''
Created on Jul. 24, 2019

@author: alex
'''

class MatchResult(object):
    '''
    classdocs
    '''


    def __init__(self, city, score, hsn=None):
        '''
        Constructor
        '''
        self.city = city 
        self.score = score 
        # Mainly for debug purposes. Highest scoring name. 
        self.hsn = hsn 
        
    def __repr__(self, *args, **kwargs):
        return str((self.city.name, self.city.country, self.hsn, self.score))
     
    def __str__(self):
        return repr(self)
    
    def dict_repr(self):
        '''Returns a dictionary representation of the match result (for JSON).
        '''
        if(self.city.name != self.hsn.upper()):
            name = self.city.origName + " (a.k.a: " + self.hsn + ")"
        else:
            name = self.city.origName 
            
        return {"name":name + ", " + self.city.country, "latitude":self.city.latitude, 
                "longitude": self.city.longitude, "score": self.score} 