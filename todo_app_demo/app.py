from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Yousif:yousif@localhost:5432/todoappdemo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<ID: {self.id}, TODO: {self.description}>'

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

@app.route('/')
def index():
    return render_template('index.html',
    data=Todo.query.order_by('id').all()
    )

if __name__ == '__main__':
    app.run()
