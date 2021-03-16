### IMPORT ###
from flask import Flask

### CODE ###

# Create flask app with name of this file
app = Flask(__name__)

# Route '/'
@app.route('/')
def index():
    return 'Hello, World!'

# Execute when script is run by Pyhton interpeter
if __name__ == '__main__':
    app.run()
