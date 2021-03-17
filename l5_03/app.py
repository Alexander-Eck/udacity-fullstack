### IMPORT ###
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

### CONSTANTS ###
ENV = 'development'
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgresql://demouser:demopwd@localhost:5432/example'

### CODE ###

# Instantiate Flask app
app = Flask(__name__)

# Update config
app.config.update(
    ENV = ENV,
    DEBUG = DEBUG,
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

# Instantiate DB connection, bind to Flask app
db = SQLAlchemy(app)

# Define todos table
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return '[Todo] {id}: {description}'.\
            format(id=self.id, description=self.description)

# Reset all defined tables
db.drop_all()
db.create_all()

# Populate todos table with a few entries
todos = (
    {'description':'Buy some milk'},
    {'description':'Get a few apples'},
    {'description':'Learn some more'},
    {'description':'Drink a glass of water'},
    {'description':'Get back to work'}
)
for t in todos:
    db.session.add(Todo(**t))
db.session.commit()

# Route '/'
@app.route('/')
def index():
    return render_template('index.html', todos=Todo.query.all())

# Execute web server when run by interpreter
if __name__ == '__main__':
    app.run()