# -*- coding: utf-8 -*-

from flask import Flask, request
from tools.autocomp import AutoComplete
from tools.dataloader import DataLoader

from tools.scoringmethods.prefixpriority import PrefixPriority

app = Flask(__name__)

# Load the cities data set. 
dataPath = 'data/cities_canada-usa.tsv'
cities = DataLoader.get_cities_tsv(dataPath)
    
@app.route('/suggestions')
def autocomplete():
    '''Returns query completion suggestions for city names in JSON format. 
    
    Given a HTTP GET request with a partial or complete query string, returns
    a JSON list of suggestions for cities that match the query, where each 
    suggestion contains the name of the city, the alternative name for the city
    if the query matched on an alternative name, the country that the city is in,
    and the decimal degree geographic coordinates of the city. 
    
    The parameters for the HTTP request are:
        q -- the (UTF-8) query string. If q is empty, '{}' is returned. 
        latitude -- [OPTIONAL] decimal degree latitude of caller. If value provided
                    is not a floating point number, it is ignored. 
        latitude -- [OPTIONAL] decimal degree longitude of caller. If value provided
                    is not a floating point number, it is ignored. 
        n -- [OPTIONAL] the number of suggestions to return. If no value is provided,
             or the value provided is badly formatted (not an integer), then 
             a default of 10 is used. If a negative value is supplied, all 
             suggestions with a score above a certain threshold are returned. 
    '''
    
    q = request.args.get('q', type=str)
    lat = request.args.get('latitude', type=float)
    longi = request.args.get('longitude', type=float)
    # Also added an argument for number of results to return.
    # Use negative number if want to return all.
    n = request.args.get('n', type=int)
    
    '''Parameters for AutoComplete. If we wanted to, could also customise parameters
    for PrefixPriority'''
    params = {'scoreMethod':PrefixPriority(), 'phoneticPenalty':0.6, 'minScore':0.1,
              'altNamePenalty':0.5, 'proximityWeight':0.1}
    
    if(n != None and type(n) is int):
        numRes = n 
    else: 
        numRes = 10 
        
    if(q == None or len(q) == 0):
        return "{}" 

    return AutoComplete().get_suggestions_json(q, lat, longi, cities, params, numRes)
    

if __name__ == '__main__':
    '''For local development, not used for deployments'''
    app.run(host='127.0.0.1', port=8080, debug=True)

