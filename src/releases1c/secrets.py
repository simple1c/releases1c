import os

# Get environment variables
USER = os.getenv('RELEASES1C_USER')
PASSWORD = os.getenv('RELEASES1C_PASSWORD')

credentials = {"login":USER,"password":PASSWORD}