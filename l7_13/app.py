### IMPORT ###
import sys
from flask import Flask, render_template, request, redirect, abort, jsonify, url_for
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

# Define lists table
class List(db.Model):
    __tablename__ = 'lists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', 
        cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f'[List] {self.id}: {self.name}'

# Define todos table
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'), nullable=False)

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
    return redirect(url_for('read_list', list_id=1))

# Route to read todos associated with a given list
@app.route('/lists/<list_id>')
def read_list(list_id):
    lists = List.query.order_by('id').all()
    cur_list = List.query.filter_by(id=list_id).first()
    todos = Todo.query.filter_by(list_id=list_id).order_by('id').all()
    # Check if all todos on the list are completed
    list_completed = all(list(map(lambda todo: todo.completed, todos)))
    return render_template('index.html', 
        lists=lists, cur_list=cur_list, list_completed=list_completed, todos=todos)

# Route to create new list item
@app.route('/lists', methods=['POST'])
def create_list():
    success = True
    json = {}
    try:
        newlist = List(**request.get_json())
        db.session.add(newlist)
        db.session.commit()
        json['id'] = newlist.id
        json['name'] = newlist.name
    except:
        success = False
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return jsonify(json) if success else abort(400)

# Route to update completed attribute of all todos from a list
@app.route('/lists/<list_id>/completed', methods=['PATCH'])
def modify_list_completed(list_id):
    success = True
    try:
        completed = request.get_json()['completed']
        todos = List.query.get(list_id).todos
        for todo in todos:
            todo.completed = completed
        db.session.commit()
    except:
        success = False
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return jsonify({ 'success': True }) if success else abort(400)

# Route to delete list with all todo items
@app.route('/lists/<list_id>', methods=['DELETE'])
def delete_list(list_id):
    success = True
    try:
        db.session.delete(List.query.get(list_id))
        db.session.commit()
    except:
        success = False
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return jsonify({ 'success': True }) if success else abort(400)

# Route to create new todo item
@app.route('/todos', methods=['POST'])
def create_todo():
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
@app.route('/todos/<todo_id>/completed', methods=['PATCH'])
def modify_todo_completed(todo_id):
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
    return jsonify({ 'success': True }) if success else abort(400)

# Route to delete todo item
@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
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