# -*- coding: utf-8 -*-


from tools.utils import strip_punctuation_spaces
import unittest

class TestStringStripping(unittest.TestCase):


    def test_nothing_to_strip(self):
        self.assertEqual(u'hello', strip_punctuation_spaces(u'hello'))
        self.assertEqual(u'뉴마켓', strip_punctuation_spaces(u'뉴마켓'))
    
    def test_strip_punctuation(self):
        self.assertEqual(u'hello231blahblah', 
                         strip_punctuation_spaces(u'@hello \"\'231 blahblah!'))
        self.assertEqual(u'마켓마켓', strip_punctuation_spaces(u'   마켓??@#  마켓'))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()