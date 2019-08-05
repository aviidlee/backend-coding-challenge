from tools.scoringmethods.scoringmethod import ScoringMethod
from tools.patternmatching import simpleprefixmatch
from tools.utils import sigmoid

class PrefixPriority(ScoringMethod):
    '''Scoring method giving higher points for beginning of pattern and text matching.

    See score() method for more details. 

    Attributes: 
        baseShift -- the number to subtract from the base score so that poor 
                     matches score in the negatives; this is necessary b.c.
                     sigmoid(0) = 0.5.
        substringBonus -- the bonus to add to the base score when the query is
                          a substring of the matchString. 
        exactMatchBonus -- the bonus to add to the base score when the query
                           is a character-for-character match of matchString.
        startMatchBonus -- bonus to add to base score when the start of query
                           matches the start of the matchString.
        minMatchLen -- the minimum number of consecutive characters that must 
                       match in order for simpleprefixmatch.get_match to return
                       a non-empty match.
        
    '''

    def __init__(self, baseShift=2, substringBonus=1.5, exactMatchBonus=2, 
                 startMatchBonus=0.2, minMatchLen=1):
        self.baseShift = baseShift
        self.subStringBonus = substringBonus
        self.exactMatchBonus = exactMatchBonus
        self.startMatchBonus = startMatchBonus
        self.minMatchLen = minMatchLen
    

    def score(self, query, matchString):
        '''Scores a text-based match between strings, giving matching beginnings high scores.
        
        Overrides ScoringMethod.score()
        
        Arguments:
            query -- the query string, e.g. 'lond'
            matchString -- UTF-8 string on which the query matched; e.g. 'london'. 
                    
        Returns: 
            A score in range [0, 1] where 0 indicates no match at all (as determined by
            get_matches method in simpleprefixmatch.py), and 1 indicates 
            a character-for-character exact match between query and matchString. 

        Preconditions: 
            -- All alphabetical characters in query and matchString are in the 
               same case (all upper or all lower). 
        '''
        
        # Get location and number of character matches 
        match = simpleprefixmatch.get_matches(query, matchString, 1)
        baseShift = self.baseShift
        substringBonus = self.subStringBonus
        exactMatchBonus = self.exactMatchBonus
        startMatchBonus = self.startMatchBonus
         
        # No match at all, return the lowest possible score. 
        if(len(match) == 0):
            return 0.0
        
        # Full, character-for-character match returns 1.0
        if(matchString == query):
            return 1.0

        # If the match is partial, the more characters match the better.
        # Single-character matches result in tonnes of results, so don't count them.
        matchLen = 0.0
        fullSubString = False 
        for tup in match: 
            if(tup[1] > 1):
                matchLen = matchLen + tup[1]
                if(tup[1] >= len(query)):
                    fullSubString = True 
                  
        # The greater portion of query matches the matchString, the better: 
        baseScore = matchLen/len(matchString)
        
        # Since a raw score of 0 will result in a score of 0.5 once sigmoid applied,
        # shift the function to the right by a bit.
        # For reference, sigmoid(-2) is approx 0.12
        baseScore = baseScore - baseShift
        
        # Give an additional bonus if the query string is a substring of matchString. 
        # Note the query may occur multiple times within the matchString;
        # e.g. query = 'lon' and matchString = 'lonlon'
        if(fullSubString):
            baseScore = baseScore + substringBonus
            # Additional bonus if strings match exactly
            if(len(query) == len(matchString)):
                baseScore = baseScore + exactMatchBonus
            
        # We give bonus points for matching at the start of the matchString, 
        # and for having a longer matching sequence 
        if(match[0][0] == 0):
            baseScore = baseScore + startMatchBonus*match[0][1]

        return sigmoid(baseScore)     
    
    
    def name(self):
        return 'Prefix Priority'
    
