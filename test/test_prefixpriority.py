import unittest
from tools.scoringmethods.prefixpriority import PrefixPriority

class TestPrefixPriorityScore(unittest.TestCase):
    
    def test_full_match(self):
        q = 'london'
        ms = 'london'

        s = PrefixPriority().score(q, ms)
        self.assertTrue(s > 0.8)
        
    def test_prefix_priority(self):
        '''Test that, given all other things being equal, a query string that 
        matches at the beginning returns a higher score.
        '''
        q = 'bris'
        ms1 = 'brisbane'
        ms2 = 'banebris'

        s1 = PrefixPriority().score(q, ms1)
        s2 = PrefixPriority().score(q, ms2)

        self.assertTrue(s1 > s2)
        
    def test_consec_scores(self):
        '''Test that, given all other things equal, the string that matches for
           more consecutive characters returns a higher score. 
        '''
        q = 'adel'
        ms1 = 'adelaide'
        ms2 = 'adeintan'

        s1 = PrefixPriority().score(q, ms1)
        s2 = PrefixPriority().score(q, ms2)
        self.assertTrue(s1 > s2)
        
    def test_length_similar(self):
        '''Test that, given all other things equal, the query string being a 
        larger proportion of the matchString scores higher.
        '''
        q = 'welli'
        ms1 = 'wellington'
        ms2 = 'wellibellismellinelli'

        s1 = PrefixPriority().score(q, ms1)
        s2 = PrefixPriority().score(q, ms2)
        self.assertTrue(s1 > s2)
        
    def test_fuller_match(self):
        '''Matches in which the query string is a prefix of the city name rather than
        should score higher than cases in which the city name is a prefix of the
        query string.
        '''
        q = 'sydn'
        ms1 = 'sydney'
        ms2 = 'syd'
 
        s1 = PrefixPriority().score(q, ms1)
        s2 = PrefixPriority().score(q, ms2)
        self.assertTrue(s1 > s2)
        
    def test_poor_match(self):
        '''If only the first character matches, should return a small score.
        '''
        q = 'ABB'
        t = 'ACTON VALE'
        s = PrefixPriority().score(q, t)
        self.assertTrue(s < 0.15)
    
    def test_negligible_match(self):
        '''Test that when essentially nothing matches, score is small.
        '''
        q = 'ABB'
        t = 'BANFF'
        s = PrefixPriority().score(q, t)
        self.assertTrue(s < 0.15)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()