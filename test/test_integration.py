# -*- coding: utf-8 -*-
'''
Tests for query completion for city names.
'''

import unittest
from tools.dataloader import DataLoader
from tools.autocomp import AutoComplete
import datetime 
from tools.query import Query 
from tools.scoringmethods.prefixpriority import PrefixPriority
from configs import ROOT_DIR
from tools.scoringmethods.jarowinkler import JaroWinkler

class Test(unittest.TestCase):
    '''Test cases to make sure query completion is working as expected on a 
    large, real data set. By as expected, we mean that the top result(s) returned
    are the ones we would desire; e.g., if q=lond, we expect london to be the 
    top result.
    '''

    @classmethod
    def setUpClass(cls):
        path = ROOT_DIR + '/data/cities_canada-usa.tsv'
        cls.cities = DataLoader.get_cities_tsv(path)
        
        # Default params for prefix priority    
        cls.pp = PrefixPriority(baseShift=2, substringBonus=1.5, exactMatchBonus=2, 
                 startMatchBonus=0.2, minMatchLen=1)
        
        # Default params for Jaro Winkler
        cls.jaro = JaroWinkler()
        
        # Change this line as necessary... 
        cls.scoringMethod = cls.pp
        print('Running tests with ' + cls.scoringMethod.name())
        
        cls.logging = False 
        if(cls.logging):
            logPath = ROOT_DIR + '/test/logs/' + str(datetime.datetime.now())
            cls.logfile = open(logPath, 'w')
        
    @classmethod
    def tearDownClass(cls):
        if cls.logging:
            cls.logfile.close() 
        
    @classmethod
    def result_to_file(cls, query, res):
        cls.logfile.write(query + '\n')
        cls.logfile.write(str(res)+'\n')
    
    
    def get_results(self, cityName, lat=None, longi=None):
        q = Query(cityName.upper(), lat, longi)

        sm = Test.scoringMethod
        
        return AutoComplete().get_query_results(q, Test.cities, scoreMethod=sm, 
                          phoneticPenalty=0.6, minScore=0.12, 
                          altNamePenalty=0.5, proximityWeight=0.1)
      
    def eq(self, actual, expected):  
        return self.assertEqual(actual, expected)
    
    def top_res_eq(self, q, first):
        '''Returns true iff name of highest-scoring match equals first 
        '''
        query = Query(q.upper(), None, None)

        sm = Test.scoringMethod
        res = AutoComplete().get_query_results(query, Test.cities, scoreMethod=sm, 
                          phoneticPenalty=0.6, minScore=0.12, 
                          altNamePenalty=0.5, proximityWeight=0.1)

        return self.assertEqual(res[0].city.name, first)
    
    def test_full_match_short(self):
        '''Full match on city with short name
        '''
        res = self.get_results('AJAX')
        self.eq(res[0].city.name, 'AJAX')
        
        
    def test_full_match_medium(self):
        '''Full match on medium-length city name.
        '''
        res = self.get_results('BANFF')
        self.eq(res[0].city.name, 'BANFF')
        
    def test_nonsense_sequence(self):
        '''Query is nonsense sequence vfdeth. We will still get non-zero scores 
        because of phonetic matching. 
        '''
        res = self.get_results('VFDETH')
        self.assertTrue(res[0].score < 0.5)
    
    def test_nonalpha(self):
        '''Test that non letter queries return no high-scoring results. 
        ''' 
        # This actually matches to one city that has 1 in its name 
        query = Query('1234!!!', None, None)
        res = AutoComplete().get_query_results(query, Test.cities, scoreMethod=Test.scoringMethod, minScore=0.3)
        self.eq(res, [])
        
        # All punctuation marks should match to nothing... 
        query = Query('##$@!!', None, None)
        res = AutoComplete().get_query_results(query, Test.cities, scoreMethod=Test.scoringMethod, minScore=0)
        self.eq(res, [])
        
        
    def test_partial_beginning(self):
        '''Query string is a prefix of city name; 
        springf --> springfield
        port --> port *
        ''' 
        self.top_res_eq('sPringf', 'SPRINGFIELD')
        res = self.get_results('port')
        self.eq(res[0].city.name[0:4], 'PORT')
        
    def test_partial_end(self):
        '''bostsford --> abbotsford 
        ''' 
        self.top_res_eq('botsford', 'ABBOTSFORD')
        
    def test_name_with_punctuation(self):
        self.top_res_eq('l\'ancien', 'LAncienneLorette'.upper())
        self.top_res_eq('st.john', 'STJOHNS')
    
    def test_partial_misspelled(self):
        '''Partial query, misspelled. beekonsf -> beaconsfield
        '''
        self.top_res_eq('beekonsf', 'BEACONSFIELD')
    
    def test_full_misspelled(self):
        '''Full query, misspelled. lundun --> london, sageeney --> Saguenay
        '''
        self.top_res_eq('lundun', 'LONDON') 
        self.top_res_eq('sageeney', 'SAGUENAY')
    
    def test_geographic_disambiguation(self):
        '''Test geographic location disambiguates between otherwise 
        closely-scoring results. 
        '''
        # There are 2 Springfields in the data set. 
        res = self.get_results('SPRINGF', 39.0, -84)
        self.assertEqual(res[0].city.name, 'SPRINGFIELD')
        
    def test_nonenglish(self):
        q = '뉴마켓'
        self.top_res_eq(q, 'NEWMARKET')
        # Full russian name is Пентиктон
        q = 'Пенти'.upper()
        self.top_res_eq(q, 'PENTICTON')
        
    def test_short_partial(self):
        '''If given very short query like 'ba' or 'a', naturally expect lots of 
        results, none of which score high, as there isn't enough information. 
        In this case though, we expect that the results at least begin with the
        query string. 
        
        This will not always be the case, as there are cities with short 
        alternate names (codes like AP) which may match highly, and also because
        the alternative name for another city might match well; e.g. an alternative
        name for Vancouver is Bankuba. 
        '''
        res = self.get_results('A', None, None)

        for i in range(3):
            self.eq(res[i].city.name[0], 'A')
        
        res = self.get_results('BA', None, None)
        for i in range(3):
            self.assertTrue(res[i].city.name[0:2] == 'BA')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()