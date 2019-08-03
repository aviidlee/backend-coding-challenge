'''
Unit tests for utility methods in AutoComplete class in autocomp.py 
'''

import unittest
from tools.autocomp import AutoComplete

class TestProximityPoint(unittest.TestCase):
    
    def test_really_far(self):
        # Antipodal points 
        n = (80, -10)
        s = (-80, 170)
        score = AutoComplete().proximity_points(n, s)
        self.assertTrue(score < 0.001 and score >= 0)
        
        # Another set of antipodal points 
        a = (5, 130.5)
        b = (-5, -49.5)
        score = AutoComplete().proximity_points(a, b) 
        self.assertTrue(score < 0.001 and score >= 0)
        
        # Poles 
        a = (90, 0)
        b = (-90, 0)
        score = AutoComplete().proximity_points(a, b) 
        self.assertTrue(score < 0.001 and score >= 0)
        
        # Antipodal points on equator 
        a = (0, -20)
        b = (0, 160)
        score = AutoComplete().proximity_points(a, b) 
        self.assertTrue(score < 0.001 and score >= 0)
    
    
    def test_really_close(self):
        tol = 0.0000001
        a = (20.45, 141.55)
        score = AutoComplete().proximity_points(a, a)
        self.assertTrue(abs(score - 1.0) < tol and score <= 1.0)
        
        b = (21.22, 140.78)
        score = AutoComplete().proximity_points(a, b)
        self.assertTrue(abs(score - 1.0) < 0.01 and score <= 1.0)

    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_empty_pattern']
    unittest.main()