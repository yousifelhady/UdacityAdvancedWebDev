from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Yousif:yousif@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Person(db.Model):
    #the default table name shall be 'person'
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name}>'

db.create_all() #create the table if not existed, otherwise do nothing

@app.route('/')
def index():
    displayPerson = Person.query.first()
    return 'Hello World, ' + displayPerson.name

if __name__ == '__main__':
    app.run()