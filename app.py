from cProfile import run
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
app= Flask(__name__)
ENV = 'dev'
if ENV == ' dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql://postgres:123456@localhost/'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URL'] = 'postgres://dygxlzjoqboofd:1bb383e2cfde782ac81b7a18667c4aabbde3b09ea87acd60e08e844af6bbd6ec@ec2-18-233-83-165.compute-1.amazonaws.com:5432/de4ss1icpf92j'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Feedback(db.Model):
    __tablename__ = 'Feedback'
    id = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    ratings = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, dealer, ratings, comments):
        self.dealer = dealer
        self.ratings = ratings
        self.comments = comments
    



@app.route("/")
def index():
    return render_template('index.html')


def submit():
    if request.metohd == 'POST':
        data = Feedback(dealer, ratings, comments)
        db.session.add(data)
        db.session.commit()
if __name__ == "__main__":
    app.debug = True
    app.run()
