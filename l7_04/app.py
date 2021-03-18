### IMPORT ###
import sys
from flask import Flask, render_template, request, redirect, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

### CONSTANTS ###
ENV = 'development'
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgresql://demouser:demopwd@localhost:5432/udacity-fullstack'

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

# Set-up migrate to manage DB schema changes
migrate = Migrate(app, db)

# Define todos table
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'[Todo] {self.id}: {self.description}'

# Takes a list of todo items (in dict form) and inserts into DB
def todos_insert(todos):
    for t in todos:
        db.session.add(Todo(**t))
    db.session.commit()

# Route '/'
@app.route('/')
def index():
    return render_template('index.html', todos=Todo.query.order_by('id').all())

# Route to create new todo item
@app.route('/todos', methods=['POST'])
def create():
    success = True
    try:
        json = request.get_json()
        todos_insert([json])
    except:
        success = False
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return json if success else abort(400)

# Route to update completed attribute of a todo item
@app.route('/todos/completed/<todo_id>', methods=['PUT'])
def update_completed(todo_id):
    success = True
    try:
        todo = Todo.query.get(todo_id)
        todo.completed = request.get_json()['completed']
        db.session.commit()
    except:
        success = False
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return redirect('/') if success else abort(400)

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete(todo_id):
    success = True
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        success = False
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return jsonify({ 'success': True }) if success else abort(400)

# Execute web server when run by interpreter
if __name__ == '__main__':
    app.run()
