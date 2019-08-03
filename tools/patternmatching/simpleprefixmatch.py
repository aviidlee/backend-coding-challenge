def get_matches(pattern, text, minLength=1):
        '''Return the position and length of occurrences of pattern in text.
        
        Only consecutive matching characters are considered, and partial matches
        of length greater than or equal to minLength are returned. 
        
        Example: 
            Input -- pattern='lon', text='ponloberrylon', minLength=1
            Output -- [(3, 2), (10, 3)]
        
        Arguments:
            pattern -- character sequence to be found in text. 
            text -- the text in which we are searching for pattern.
            minLength -- the minimum number of consecutive matching characters 
                         required for the pattern to be considered "matched".
        Returns: 
            A list of tuples otf (p, l), where p is the index of the character in 
            text at which the first letter of p is found, and l is the length of the match. 
            In the event of no match, an empty list is returned. 
            
        Preconditions: 
            -- all alphabetical characters in pattern and text are in the same case.
        '''
        matches = []
        # Length of consecutive matching characters 
        matchLen = 0
        # the index of the character in pattern we are trying to match
        i = 0
        # the index of the character in the text we are trying to match
        j = 0
        
        if(len(pattern) == 0 or len(text) == 0):
            return []
        
        while(j < len(text)):
            if(i == len(pattern)):
                '''We still have text to see, but we are at the end of the pattern;
                Therefore reset i and matchLen.
                '''
                i = 0
                if(matchLen == len(pattern)):
                    matches.append((j-matchLen, matchLen))
                    
                matchLen = 0
            
            # Character matches, keep matching... 
            if(pattern[i] == text[j]):
                matchLen = matchLen + 1
                i = i + 1
                
            else: 
                if(matchLen >= minLength):
                    # Add result tuple to matches 
                    matches.append((j-matchLen, matchLen))
                
                # Reset counter to look from beginning of pattern again.
                if(matchLen > 0):
                    i = 0
                    matchLen = 0
                    # test[j] may match pattern[i]
                    j = j - 1  
            
            j = j + 1
        
        if(matchLen >= minLength): 
            if(j == len(text) - 1):
                matches.append((j+1-matchLen, matchLen))
            else:
                matches.append((j-matchLen, matchLen))
                    
        return matches 
