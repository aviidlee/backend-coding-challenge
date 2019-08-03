'''
Miscellaneous utility functions.

Attributes: 
    EARTH_RADIUS_KM -- approximate radius of the earth in km. 
    PUNCTUATION_SPACES -- unicode punctuation and whitespace characters. 
    
Methods:
    haversine -- computes haversine distance between two coordinates. 
    sigmoid -- computes sigmoid function, i.e., 1.0/(1.0 + exp(-x))
'''

from math import radians, cos, sin, asin, sqrt, exp 
import unicodedata
import sys 

EARTH_RADIUS_KM = 6371.0088
PUNCTUATION_SPACES = dict.fromkeys(i for i in range(sys.maxunicode)
                            if unicodedata.category(chr(i)).startswith('P')
                            or unicodedata.category(chr(i)).startswith('Z'))
def haversine(c1, c2):
    '''Returns the haversine distance between two coordinates. 
    
    Simplified version of method by Balthazar Rouberol, at 
    https://github.com/mapado/haversine
    
    Arguments:
        c1 -- tuple of decimal degree coordinates
        c2 -- tuple of decimal degree coordinates
    
    Preconditions:
        -- c1 != None and c2 != None
        -- c1 and c2 are 2-tuples of numeric values.
    ''' 
    
    lat1, long1 = c1 
    lat2, long2 = c2 
    lat1, long1, lat2, long2 = map(radians, (lat1, long1, lat2, long2))
    
    lat = lat2 - lat1
    longi = long2 - long1
    d = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(longi * 0.5) ** 2
    
    return 2 * EARTH_RADIUS_KM * asin(sqrt(d))

def sigmoid(x):
    '''Compute sigmoid of x.'''
    return 1.0/(1.0 + exp(-x))

def strip_punctuation_spaces(text):
    return text.translate(PUNCTUATION_SPACES)

    