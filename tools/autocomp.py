# -*- coding: utf-8 -*-

from metaphone import doublemetaphone
from tools.utils import haversine, sigmoid, strip_punctuation_spaces
from tools.matchresult import MatchResult
from tools.query import Query

import json 
from tools.scoringmethods.scoringmethod import ScoringMethod
from tools.scoringmethods.prefixpriority import PrefixPriority

class AutoComplete(object):
    '''
    Methods for query completion for city names. 
    
    Given a query string, a list of Cities and (optionally) the latitude and
    longitude of the caller, provides a list of suggestions for cities, with a
    name, latitude, longitude, and a score in range [0, 1] for each suggested
    city, where the score represents the confidence level that the suggested
    city is the one the query is searching for - the higher the score, the 
    more confident. 
    
    Methods:
        get_suggestions_json -- returns auto-complete suggestions for query in 
                                JSON format.
        get_query_results -- gets auto-complete suggestions for a query, taking into
                             account query string, location (if provided), and
                             other factors. 
        json_repr -- returns a JSON representation of given auto-complete suggestions.
        proximity_points -- given 2 coordinates, returns a value in [0, 1] where 
                            the larger the value, the closer the coordinates.
                                
    '''
    
    def get_suggestions_json(self, q, lat, longi, cities, params, numRes=10):
        '''Returns a list of cities matching query q in JSON format.
        
        Arguments: 
            q -- the query string; e.g. 'london'
            lat -- decimal degree latitude
            longi -- decimal degree longitude 
            cities -- list of City objects to try to match the query to
            params -- dictionary containing parameters for get_query_result method;
                      the keys should be the names of the arguments thereof.
            numRes -- the number of results to return. 
                      If numRes > the number of results returned by algorithm,
                      return all available results. 
                      If numRes is negative, return all results. 
                      
        Preconditions:
            -- q is non-null and non-empty
            -- lat is a real number in range [-90, 90]
            -- longi is a real number in range [-180, 180]
            -- params should contain all necessary parameters to call 
               get_query_results; this method does NOT do error-checking
               for this.
        '''
          
        query = Query(q, lat, longi)
        results = self.get_query_results(query, cities, 
                                    params['scoreMethod'], params['phoneticPenalty'], 
                                    params['minScore'], params['altNamePenalty'], 
                                    params['proximityWeight'])
        if(numRes < 0):
            numRes = len(results)
            
        return self.json_repr(results[0:numRes])
    
    
    def get_query_results(self, query, data, scoreMethod=PrefixPriority, 
                          phoneticPenalty=0.2, minScore=0.15, 
                          altNamePenalty=0.5, proximityWeight=0.1):
        '''Get all cities matching the query with a score > minScore
        
        Arguments:
            query -- Query object with user's query string, and optionally 
                     latitude, and longitude.
            data -- list of City objects to try to match query to. 
            scoreMethod -- the scoring method to use. If no argument is supplied, 
                            prefix_priority_method is used.
            phoneticPenalty -- number to multiply to scores obtained from phonetic
                               matches; this allows us to favour exact matches.
            altNamePenalty -- number to multiply to scores obtained by matching 
                              to an alternative name of city; favours matches to
                              the most well-known name of cities. 
            proximityWeight -- how much influence geographical closeness has on
                               the final score, if applicable. 
        
        Returns:
            A list of MatchResults, each MatchResult containing the city, 
            match (the return type of get_matches), and score. 
            
        Preconditions:
            -- query.q != None and query.q != ''
        '''
        
        results = []
        # Phonetic representation of query
        pq1, pq2 = doublemetaphone(query.q)
        if(len(pq2) > 0):
            pq = (pq1, pq2)
        else:
            pq = pq1,
        
        # Convert query to uppercase, strip punctuation and whitespace.
        queryStr = strip_punctuation_spaces(query.q)
        queryStr = queryStr.upper()
        
        for city in data: 

            # Try matching original query string to the city name. 
            maxScore = scoreMethod.score(queryStr, city.name)
            
            # The name of the city that got the highest score.
            bestName = city.origName 
            
            # Then try matching alternative names 
            for name in city.altNames: 
                score = altNamePenalty * scoreMethod.score(queryStr, name)

                if(score > maxScore):
                    maxScore = score 
                    bestName = name 
            
            '''    
            Now try matching based on phonetic names, and penalise the 
            score slightly. Also require that for phonetics, we need a longer
            character sequence to match (else way too many irrelevant results). 
            '''
            if(len(pq1) >=2):
                for origName in city.phonetics:
                    # For each phonetic representation of the alternative name
                    for name in city.phonetics[origName]:
                        # for each phonetic representation of the query string    
                        for q in pq:      
                            score = phoneticPenalty * scoreMethod.score(q, name)  
                            if(score > maxScore):
                                maxScore = score 
                                bestName = origName
                                             
            # If query location provided, score closer cities higher. 
            # Also give location more weight when score is already high. 
            if(query.coord != None and maxScore > minScore):
                proxPoints = self.proximity_points(query.coord, 
                                                  (city.latitude, city.longitude))
                
                # Add proximity points and renormalise to [0, 1] range.
                maxScore = (maxScore + proxPoints*maxScore*proximityWeight)/(1.0 + proximityWeight)
            
            if(maxScore > minScore):
                results.append(MatchResult(city, maxScore, bestName))
                    
        # Sort results in descending order.                   
        return sorted(results, key=lambda matchresult: matchresult.score, reverse=True)

    
    def proximity_points(self, query, candidate):
        '''Returns a score between 0 and 1 based on physical proximity of query and candidate.
        
        Given two geographic coordinates, compute the haversine distance between them and 
        return a number in range [0, 1], where 0 means as far apart as possible
        and 1 means exact same location. 
        
        Arguments:
            query -- latitude and longitude of the query location given as a 
                     decimal degree tuple.
            candidate -- latitude and longitude of the candidate location given 
                         as a decimal degree tuple.
        
        Returns:
            A float in range [0, 1]. 
            
        Preconditions 
            -- query != None && candidate != None
            -- both query and candiate are valid decimal degree coordinates; 
               that is, otf (x, y) where -90 <= x <= 90 and -180 <= y <= 180.
        '''
        
        ''''The (approximate) maximum distance any two locations on the surface 
        of a sphere of radius 6371 km can be. 
        '''
        MAX_DIST = 20016
        dist = haversine(query, candidate)
        
        return 1.0 - (dist/MAX_DIST)
    
    
    def json_repr(self, matchResults):
        '''Returns a JSON representation of the matchResults.
        '''
        return json.dumps(matchResults, default=MatchResult.dict_repr)
         
    
    
    
