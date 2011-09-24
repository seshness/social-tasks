from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float

# DB crap
#SOME FLASK SQLACHEMY METHODS TO SAVE TO DATABASE

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://socialtasks:alert48:pees@ec2-75-101-240-217.compute-1.amazonaws.com/socialtasks'
db = SQLAlchemy(app)

assignee_tasks = db.Table('assignee_tasks',
                      db.Column('task_id', db.Integer,
                                db.ForeignKey('task.task_id')),
                      db.Column('facebook_id', db.Integer,
                                db.ForeignKey('fbuser.facebook_id'))
                      )

hidefrom_tasks = db.Table('hidefrom_tasks',
                      db.Column('task_id', db.Integer,
                                db.ForeignKey('task.task_id')),
                      db.Column('facebook_id', db.Integer,
                                db.ForeignKey('fbuser.facebook_id'))
                      )

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    creation_time = db.Column(db.DateTime)

    assignees = db.relationship('Fbuser', secondary=assignee_tasks,
                                backref=db.backref('assignee_task',
                                                   lazy='dynamic'))
    hidefrom  = db.relationship('Fbuser', secondary=hidefrom_tasks,
                                backref=db.backref('hiddefrom_task',
                                                   lazy='dynamic'))

    assigner_id = db.Column(db.Integer, db.ForeignKey('fbuser.facebook_id'))
    done = db.Column(db.Boolean)
    task_name = db.Column(db.Text)
    contents = db.Column(db.Text)
    comments = db.relationship('Comment', backref='task',
                               lazy='dynamic')

    def __init__(self, task_id, creation_time, assigner_id,
                 contents):
        self.task_id = task_id
        self.creation_time = creation_time
        self.assigner_id = assigner_id
        self.contents = contents

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id'))
    creation_time = db.Column(db.DateTime)
    author = db.Column(db.Integer, db.ForeignKey('fbuser.facebook_id'))
    contents = db.Column(db.Text)

    def __init__(self, comment_id, task_id, creation_time,
                 author, contents):
        self.comment_id = comment_id
        self.task_id = task_id
        self.creation_time = creation_time
        self.author = author
        self.contents = contents

class Fbuser(db.Model):
    facebook_id = db.Column(db.String(20), primary_key=True)
    tasks = db.relationship('Task', backref='assigner', lazy='dynamic')


    def __init__(self, facebook_id):
        self.facebook_id = facebook_id

    def __repr__(self):
        return '<FbUser %r>' % repr(self.facebook_id)


