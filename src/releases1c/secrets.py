import json
import os

__credentials_filename = '__credentials.json'
credentials = {"login":"","passwod":""}
'''
Credentials saved in file __credentials.json:
{"login": "<login>", "password": "<password>"}
'''
if os.path.isfile(__credentials_filename):
    with open(__credentials_filename,"r") as credentials_file:
        credentials = json.loads(credentials_file.read())