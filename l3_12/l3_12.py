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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define persons table
class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True)
    age = db.Column(db.Float, db.CheckConstraint('age>0'))

    # Define custom __repr__
    def __repr__(self):
        return '<Person> {name}, {email}'.format(name=self.name, email=self.email)

# Reset persons table, to ensure we start afresh
db.drop_all()
db.create_all()

# Populate persons table with an entry
person1 = Person(name='Alexander', email='alex@awesone.com', age='35.0')
db.session.add(person1)
db.session.commit()

# Route '/'
@app.route('/')
def index():
    return 'Hello, {name}!'.format(name=Person.query.first().name)

# Execute when script is run by Pyhton interpeter
if __name__ == '__main__':
    app.run()
