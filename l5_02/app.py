### IMPORT ###
from flask import Flask, render_template

### CONSTANTS ###
ENV = 'development'
DEBUG = True

### CODE ###

# Instantiate Flask app
app = Flask(__name__)

# Update config
app.config.update(
    ENV = ENV,
    DEBUG = DEBUG
)

# Get some list items
todos = [
    {'description':'Buy some milk'},
    {'description':'Get a few apples'},
    {'description':'Learn some more'},
    {'description':'Get back to work'}
]

# Route '/'
@app.route('/')
def index():
    return render_template('index.html', todos=todos)

# Execute web server when run by interpreter
if __name__ == '__main__':
    app.run()