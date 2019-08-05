from tools.utils import strip_punctuation_spaces

class MatchResult(object):
    '''
    Represents a result of a query - the city that matched and other data.

    Attributes:
        city -- the city that matched.
        score -- the score of the match, in range [0, 1]. 
        hsn -- highest scoring name; the name of the city (many cities have 
               alternate names) which resuted in the highest scoring match.
               Should be the unprocessed version, with punctuation and spaces
               intact. 

    Methods:
        dict_repr -- Returns a dictionary representation of this. 

    '''


    def __init__(self, city, score, hsn=None):
        '''
        Constructor
        '''
        self.city = city 
        self.score = score 
        # Highest scoring name. 
        self.hsn = hsn 
        
    def __repr__(self, *args, **kwargs):
        return str((self.city.name, self.city.country, self.hsn, self.score))
     
    def __str__(self):
        return repr(self)
    
    def dict_repr(self):
        '''Returns a dictionary representation of the match result (for JSON).
        '''
        # If highest-scoring name is not the best-known name of city, add it.
        # Otherwise the search result may be very confusing to user.
        if(self.city.origName != self.hsn):
            name = self.city.origName + " (a.k.a: " + self.hsn + ")"
        else:
            name = self.city.origName 
            
        return {"name":name + ", " + self.city.country, "latitude":self.city.latitude, 
                "longitude": self.city.longitude, "score": self.score} 
