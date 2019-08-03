import unittest
from tools.dataloader import DataLoader, NoneUniqueIDException
from configs import ROOT_DIR

class TestImport(unittest.TestCase):
    
    def test_sample_file(self):
        # File consists of first 20 rows (so 19 cities) of cities_canada-usa.tsv

        path = ROOT_DIR + '/data/sample.tsv'
        cities = DataLoader.get_cities_tsv(path)
        first = cities[0]
        self.assertEqual(first.name, 'ABBOTSFORD')
        self.assertEqual(first.ID, 5881791)
        self.assertEqual(first.latitude, 49.05798 )
        self.assertEqual(first.longitude, -122.25257)
        self.assertEqual(first.country, 'CA')
    
    
    def test_nonunique_id(self):
        '''Tests that exception raised if IDs are not unique.'''
        
        path = ROOT_DIR + '/data/nonunique_id.tsv'
        
        with self.assertRaises(NoneUniqueIDException) as cm:
            DataLoader.get_cities_tsv(path)

 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()