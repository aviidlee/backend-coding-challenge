class Query(object):
    '''Represents a query with query string and optional geographicla coordinates. 

    Treat as immutable. 
    
    Attributes:
        q -- UTF-8 query string; e.g. 'lond', 'banff'
        coord -- decimal degree coordinates, in a 2-tuple. 
    '''

    def __init__(self, q, lat, longi):
        '''Create a query with the search string, and optionally latitude and longitude.
        
        Arguments:
            q -- Non-empty UTF-8 string
            lat -- latitude; use None if not provided, or is not a float.
            longi -- longitude; use None if not provided, or is not a float.
        
        Postconditions: 
            -- len(this.q) != 0
            -- Either this.coord == None, or this.coord is a 2-tuple of floats.
        
        Raises:
            ValueError if len(q) == 0.
        '''
        if (len(q) == 0):
            raise ValueError("Query string cannot be empty.")
        
        self.q = q 
        if(lat != None and longi != None):
            self.coord = (lat, longi)
        else:
            self.coord = None
            
    def __repr__(self, *args, **kwargs):
        return repr((self.q, self.lat, self.longi))