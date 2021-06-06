import os

SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Run in development mode, enable debug
ENV = 'development'
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://demouser:demopwd@localhost:5432/udacity-fullstack'

# Get rid of deprecated warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
