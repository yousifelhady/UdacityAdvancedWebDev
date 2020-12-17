from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Yousif:yousif@localhost:5432/todoappdemo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<ID: {self.id}, TODO: {self.description}>'

db.create_all() #create tables if not exist

@app.route('/todos/create', methods=['post'])
def create_todo():
    myDescription = request.form.get('description', '')
    newTodo = Todo(description=myDescription)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for('indexy'))

@app.route('/')
def indexy():
    return render_template('index.html',
    data=Todo.query.all()
    )

if __name__ == '__main__':
    app.run()
