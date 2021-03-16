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

# Define Person class
class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True)

    def __repr__(self):
        return '<Person %r>' % self.name

# Reset table, to ensure we start afresh
db.drop_all()
db.create_all()

# Route '/'
@app.route('/')
def index():
    return 'Hello, {name}'.format(name='Alex')

# Execute when script is run by Pyhton interpeter
if __name__ == '__main__':
    app.run()
