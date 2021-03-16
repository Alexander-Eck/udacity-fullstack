### IMPORT ###
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

### CONSTANTS ###
SQLALCHEMY_DATABASE_URI = 'postgresql://demouser:demopwd@localhost:5432/example'

### CODE ###

# Instantiate Flask app
app = Flask(__name__)

# Instantiate DB connection, bind it to Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

# Route '/'
@app.route('/')
def index():
    return 'Hello, {name}'.format(name='Alex')

# Execute when script is run by Pyhton interpeter
if __name__ == '__main__':
    app.run()
