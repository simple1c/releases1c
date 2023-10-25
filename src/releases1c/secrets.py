import os

# Get environment variables
USER     = os.getenv('RELEASES1C_USERNAME')
PASSWORD = os.getenv('RELEASES1C_PASSWORD')

credentials = {"login":USER,"password":PASSWORD}