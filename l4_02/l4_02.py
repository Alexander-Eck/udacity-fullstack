### IMPORT ###
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

### CONSTANTS ###
SQLALCHEMY_DATABASE_URI = 'postgresql://demouser:demopwd@localhost:5432/example'
ENV = 'development'
DEBUG = True

### CODE ###

# Instantiate Flask app
app = Flask(__name__)

# Instantiate DB connection, bind to Flask app
app.config.update(
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    ENV = ENV,
    DEBUG = DEBUG
)
db = SQLAlchemy(app)

# Define persons table
class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True)
    age = db.Column(db.Float, db.CheckConstraint('age>0'))

    def __repr__(self):
        return '[Person] {name}, {email}'.format(name=self.name, email=self.email)

# Reset persons table, so we start afresh
db.drop_all()
db.create_all()

# Populate persons table with a few entries
persons = (
    {'name':'Alexander', 'email':'alex@awesome.com'},
    {'name':'Michael'},
    {'name':'Bernd'},
    {'name':'Christiane'},
    {'name':'Luisa'},
    {'name':'Sofia'},
    {'name':'Jasmin'},
    {'name':'Kathrin'},
    {'name':'Anna'}
)
for p in persons:
    db.session.add(Person(**p))
db.session.commit()

# Route '/'
@app.route('/')
def index():
    # Perform a few queries and return results
    commands = (
        'Person.query.all()',
        'Person.query.count()',
        'Person.query.limit(5).all()',
        'Person.query.filter(Person.name.like("A%")).all()',
        'Person.query.filter_by(name="Alexander").all()'        
    )
    results = ''
    for c in commands:
        results += c + ': <br />'
        results += str(eval(c))
        results += '<br /><br />'
    return results

# Execute web server when run by interpreter
if __name__ == '__main__':
    app.run()
