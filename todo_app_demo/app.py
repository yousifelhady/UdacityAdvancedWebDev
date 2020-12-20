from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Yousif:yousif@localhost:5432/todoappdemo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

    def __repr__(self):
        return f'<ID: {self.id}, List Name: {self.name}>'

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<ID: {self.id}, TODO: {self.description}, Completed: {self.completed}>'

#db.create_all() #create tables if not exist

@app.route('/todos/create', methods=['post'])
def create_todo():
    error = False
    body = {}
    try:
        myDescription = request.get_json()['description']
        newTodo = Todo(description=myDescription)
        db.session.add(newTodo)
        db.session.commit()
        body['description'] = newTodo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:    
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)

@app.route('/todos/<todoId>/set-completed', methods=['post'])
def check_todo(todoId):
    try:
        status = request.get_json()['completed']
        targetedTodo = Todo.query.get(todoId)
        targetedTodo.completed = status
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todoId>/delete', methods=['delete'])
def delete_todo(todoId):
    try:
        todo = Todo.query.get(todoId)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({ 'success': True })

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html',
    lists=TodoList.query.order_by('id').all(),
    todos=Todo.query.filter_by(list_id=list_id).order_by('id').all(),
    active_list=TodoList.query.get(list_id))

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))

if __name__ == '__main__':
    app.run()
