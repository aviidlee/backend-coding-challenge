'''
Non-GCP configurations and unfortunately-necessary global variables. 

This file must live in the root directory of the project; i.e., where one
would also find app.yaml.
'''
import os 

# Project root 
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
