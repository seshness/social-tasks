from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float

# DB crap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://socialtasks:alert48:pees@ec2-75-101-240-217.compute-1.amazonaws.com/socialtasks'
db = SQLAlchemy(app)
"""
class Task(db.Model):
    task_id = db.Column('task_id', Integer, primary_keys=True)
    created_date = db.Column('created_date', Date)
    assigner =  
    assignee =
    hide_from
    done 
    task_contents
    comments

class Comment(db.Model):
    comment_id = db.Column('comment_id', Integer, primary_keys=True)
    
"""
class User(db.Model):
    facebook_user_id = db.Column('facebook_user_id', Integer, primary_keys=True)

    def __init__(self, fbid):
        self.user_id = fbid

    def __repr__(self):
        return '<User %r>' % __repr__(self.user_id)
