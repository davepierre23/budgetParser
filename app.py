from cProfile import run
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
app= Flask(__name__)
ENV = 'dev'
if ENV == ' dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jamalb@localhost:5432/postgres'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dygxlzjoqboofd:1bb383e2cfde782ac81b7a18667c4aabbde3b09ea87acd60e08e844af6bbd6ec@ec2-18-233-83-165.compute-1.amazonaws.com:5432/de4ss1icpf92j'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.String(200),primary_key=True)
    transactonDescript = db.Column(db.String(200))
    amount = db.Column(db.Float)
    transactonDate = db.Column(db.DateTime()) 
    bankAction = db.Column(db.String(1))
 


    def __init__(self, transactonDescript, amount, transactonDate , bankAction):
        self.transactonDescript = transactonDescript
        self.amount = amount
        self.transactonDate = transactonDate
        self.bankAction = bankAction
    


db.session.commit()
db.create_all()
@app.route("/")
def index():
    return render_template('index.html')


def submit():
    if request.metohd == 'POST':
         
        data = create(row)
        db.session.add(data)
        db.session.commit()
if __name__ == "__main__":
    app.debug = True
    app.run()


def create(row):
    return Transaction(row.transactonDescript, row.amount, row.transactonDate, row.bankAction)