from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float

# DB crap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://socialtasks:alert48:pees@ec2-75-101-240-217.compute-1.amazonaws.com/socialtasks'
db = SQLAlchemy(app)

assignee_tasks = db.Table('assignee_tasks',
                      db.Column('task_id', db.Integer, db.ForeignKey('task.task_id')),
                      db.Column('facebook_id', db.Integer, db.ForeignKey('user.facebook_id'))
                      )

hidefrom_tasks = db.Table('hidefrom_tasks',
                      db.Column('task_id', db.Integer, db.ForeignKey('task.task_id')),
                      db.Column('facebook_id', db.Integer, db.ForeignKey('user.facebook_id'))
                      )

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    creation_time = db.Column(db.DateTime)

    assignees = db.relationship('User', secondary=assignee_tasks,
                                backref=db.backref('assignee_task', lazy='dynamic'))
    hidefrom  = db.relationship('User', secondary=hidefrom_tasks,
                                backref=db.backref('hiddefrom_task', lazy='dynamic'))

    assigner_id = db.Column(db.Integer, db.ForeignKey('user.facebook_id'))
    done = db.Column(db.Boolean)
    contents = db.Column(db.Text)
    comments = db.relationship('Comments', backref='task', lazy='dynamic')

class Comments(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id'))
    creation_time = db.Column(db.DateTime)
    author = db.Column(db.Integer, db.ForeignKey('user.facebook_id'))
    contents = db.Column(db.Text)

class User(db.Model):
    facebook_id = db.Column(db.Integer, primary_key=True)
    tasks       = db.relationship('Task', backref='assigner', lazy='dynamic')


    def __init__(self, facebook_id):
        self.facebook_id = facebook_id

    def __repr__(self):
        return '<User %r>' % repr(self.facebook_id)


