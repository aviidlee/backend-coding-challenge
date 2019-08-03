import unittest
from tools.patternmatching import simpleprefixmatch as spm

class SimplePrefixMatchTest(unittest.TestCase):

    def test_empty_pattern(self):
        matches = spm.get_matches('', 'adj')
        self.assertEqual(matches, [])
        
    def test_empty_text(self):
        matches = spm.get_matches('adj', '')
        self.assertEqual(matches, [])
        
    def test_pattern_longer(self):
        '''Case in which pattern is longer than text, full match.'''
        matches = spm.get_matches('bambambam', 'bam')
        self.assertEqual(matches,[(0, 3)])
    
    def test_pattern_longer_partial(self):
        matches = spm.get_matches('baroomfoom', 'cabar')
        self.assertEqual(matches, [(2, 3)])
    
    def test_pattern_longer_full(self):
        matches = spm.get_matches('sydn', 'syd')
        self.assertEqual(matches, [(0, 3)])
        
    def test_pattern_longer_none(self):
        matches = spm.get_matches('baroomfoom', 'zim')
        self.assertEqual(matches, [])
        
    def test_no_match(self):
        matches = spm.get_matches('london', 'sydney') 
        self.assertEqual(matches, [])
    
    def test_match_prefix(self):
        '''Pattern is a prefix of text''' 
        matches = spm.get_matches('lond', 'londonderry') 
        self.assertEqual(matches, [(0, 4)])
        
    def test_match_suffix(self):
        '''Pattern is a suffix of text'''
        matches = spm.get_matches('shire', 'oxfordshire')
        self.assertEqual(matches, [(6, 5)]) 
    
    def test_mixed(self):
        '''Multiple partial pattern matches in text'''
        matches = spm.get_matches('jam', 'ajajamkaj', 1)
        self.assertEqual(matches, [(1,2), (3, 3), (8, 1)])
    
    def test_sequential(self):
        matches = spm.get_matches('lond', 'lonlon')
        self.assertEqual(matches, [(0, 3), (3, 3)])
        
        
    def test_min_match_not_satisfied(self):
        '''Tests returned values correct if there are some matching characters,
        but fewer than the minimum required
        '''
        
        matches = spm.get_matches('PNF', 'SPLNFRT', 2)
        self.assertEqual(matches, [])
        
        matches = spm.get_matches('PNF', 'PTTP', 2)
        self.assertEqual(matches, [])
        
        
    def test_min_match_satisfied(self):
        '''Tests returned value correct when minMatch > 1
        '''
        matches = spm.get_matches('PNF', 'PNF', 2)
        self.assertEqual(matches, [(0, 3)])
        matches = spm.get_matches('AB', 'ABTABAA', 2)
        self.assertEqual(matches, [(0, 2), (3, 2)])
        matches = spm.get_matches('AB', 'ATTABTTAJ', 2)
        self.assertEqual(matches, [(3, 2)])
        matches = spm.get_matches('ABC', 'ATTABTTAJABC', 2)
        self.assertEqual(matches, [(3, 2), (9, 3)])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()