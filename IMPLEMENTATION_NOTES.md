# Implementation Notes 

## Overview 
The program uses a combination of pattern matching on the query string and city
names and pattern matching on the phonetic representations of the query string
and city names. There are currently two pattern-matching algorithms available -
Prefix Priority (in tools.scoringmethods.prefixpriority) and Jaro-Winkler, (in tools.scoringmethods.jarowinkler). 
At the time of writing, only the parameters for Prefix Priority are tuned,
and that is the method that the version deployed on GCP uses. 

When a data set (from geonames, for instance) is loaded, the cities are preprocessed to store their names in uppercase with whitespace and punctuation stripped.A phonetic representation of all of the city's names are also stored (we use the double metaphone algorithm). When a query is executed, a similarly preprocessed version of the query is first pattern-matched to the (preprocessed) city's names, and then the phonetic representation of the query is pattern-matched to the phonetic representations of the city's name, in each case returning a score in range [0.0, 1.0]. The best score is recorded, as well as the name of the city that attained that best score. This scoring is done for each city in the data set, and then the cities are returned in descending order of scores.  

Although the writer of this program discovered it too late in development to
make much use of it, there is a paper called *A comparison of Personal Name Matching: Techniques and Practical Issues* by Peter Christen (available at http://users.cecs.anu.edu.au/~Peter.Christen/publications/tr-cs-06-02.pdf) which discusses various methods for matching names, which is applicable in this task. 

Parameters for the scoring algorithms are tunable, and passed in from the top-level method AutoComplete().get_query_suggestions() via a dictionary; refer to docstring comments for details. Each pattern-matching algorithm (Prefix Priority, Jaro-Winkler etc.) has its own parameters, which are set via the constructors of their respective classes. 

## Notes on some technical choices 
- Levenshtine is a common choice for pattern-matching, but is not used here because  Jaro-Winkler and the simple custom method employed by Prefix Priority are faster. 
- Winkler has shown that spelling errors are less likely to occur at the beginning of words, and so we accordingly give higher scores when the beginning of a query matches the beginning of a city name. 
- The parameters used by the scoring method are tuned more or less by trial and error. For a genuinely useful query completion algorithm, we need to learn these parameters from actual user data (which we don't have). Christen (2006) also notes this as a major point in the recommendations section of his paper. 

## Directories 
- All application logic is in `tools`.
- All tests are in `test` 
- Data on cities, including those used for testing, are in `data`. 

## TODO
- Profile the code! 
- Tune parameters for Jaro-Winkler. 
