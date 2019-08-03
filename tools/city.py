from metaphone import doublemetaphone
from tools.utils import strip_punctuation_spaces

class City(object):
    '''A city and pre-computed attributes to aid in queries. 
        
    In addition to provided arguments, City also stores the capitalised
    versions of its name and alternative names and their associated phonetic
    representations as computed by the double metaphone algorithm. 
    NB: Treat class as immutable.
    
    Attributes:
        ID -- unique ID for this city. Two cities are considered 
              identical if they have identical IDs. 
        name -- the (most well-known) name for this city; e.g. "VANCOUVER"
                UTF-8, in all-uppercase with whitespace and punctuation stripped.
        altNames -- list of other names by which this city is known, stored 
                    in all-uppercase with whitespace and punctuation stripped.
        latitude -- latitude of this city in decimal degrees. 
        longitude -- longitude of this city in decimal degrees. 
        country -- ISO country code 
        origName -- the most well-known name of this city before it was 
                    preprocessed; i.e., in original case and with spaces,
                    punctuation etc. 
        phonetics -- a dictionary in which the key is one of the names of 
                     this city in its original form (with case, spaces, etc.),
                     and the value a tuple consisting of the phonetic 
                     representations of this city.
    '''    
    
    def __init__(self, ID, name, altNames, latitude, longitutde, country):
        # Unique ID for this city. Must be hashable.
        self.ID = ID
        # UTF-8 Name, stored in all-uppercase for simplicity. 
        self.name = self.preprocess(name)
        # Alternate names, list of UTF-8 strings, all-uppercase (where applicable) 
        self.altNames = []
        for altName in altNames: 
            if(len(altName) > 0):
                self.altNames.append(self.preprocess(altName)) 
            
        # Also store original name, as written in the file. 
        # If we decide to strip whitespace, punctuation, etc. want to be able to
        # return the actual name of city.
        self.origName = name 
         
        self.latitude = latitude
        self.longitude = longitutde
        # ISO-3166 2-letter country code 
        self.country = country 
        
        # dic of phonetic (double metaphone) representation of city's name(s)
        # key is original name (with no preprocessing), value is phonetic name. 
        self.phonetics = {}        
        # Store metaphone representation of city's name and alt names.
        self.phonetics[self.origName] = doublemetaphone(self.origName)
        
        for name in altNames:
            self.phonetics[name] = doublemetaphone(name)
    
    def preprocess(self, string):
        '''Removes whitespace and punctuation from string, convert to uppercase.'''
        s = strip_punctuation_spaces(string)    
        s = s.upper()
        return s 
      
    def __str__(self, *args, **kwargs):
        return self.origName + " in " + self.country + " (ID=" + str(self.ID) + ")"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.ID == other.ID
        