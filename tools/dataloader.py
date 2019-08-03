# -*- coding: utf-8 -*-

from tools.city import City
import csv 
import sys

class DataLoader(object):
    '''Methods for reading city data and returning a list of City objects.
    
    Methods:
        get_cities_tsv -- read tab-separated geonames file. 
        
    '''
    
    @classmethod
    def get_cities_tsv(cls, fileName):
        '''Returns a list of city objects from a geonames tsv file.
        
        The file is expected to be tab-separated, with the first row being the
        field names. The field names should contain: name, id, alt_name, lat, long,
        and country. The field alt_name gives the alternative names of the 
        city, comma-separated. The character encoding is UTF-8.
        
        Arguments:
            fileName -- path to the TSV file.
        
        Returns:
            A list of city objects corresponding to cities in the input file. 
            
        Raises:
            NoneUniqueIDException -- raised if file contains two cities with the
                                     same id field.
        
        '''
        cities = []
        # Hash set of city IDs, to ensure IDs are unique. 
        IDs = set()
        
        csv.field_size_limit(sys.maxsize)
        
        with open(fileName, 'rt') as f:
            reader = csv.DictReader(f, delimiter='\t',
                                quoting=csv.QUOTE_NONE)
            for row in reader: 
                altnames = row['alt_name'].split(',')
                ID = int(row['id'])
                
                if(ID in IDs):
                    raise NoneUniqueIDException('ID ' + row['id'] + ' duplicated')
                
                IDs.add(ID)
                cities.append(City(ID, row['name'], altnames, 
                                   float(row['lat']), float(row['long']), 
                                   row['country']))
                
            
        return cities 
    

class NoneUniqueIDException(Exception):
    '''Exception raised if two cities in a file have the same ID.'''
    pass 