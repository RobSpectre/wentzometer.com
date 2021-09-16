'''
Configuration Settings
'''

# Begin Heroku configuration - configured through environment variables.
import os
TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY', None)
TWITTER_SECRET = os.environ.get('TWITTER_SECRET', None)
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN', None)
TWITTER_ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET', None)
