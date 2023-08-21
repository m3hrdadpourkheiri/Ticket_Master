from WebApp import db,login_manager
import datetime
from flask_login import UserMixin
import jdatetime



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


'''class Organization_Unit(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),unique=True)
    users=db.relationship('User',backref='ou',lazy=True)'''




class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    fullname = db.Column(db.String(30),unique=False,nullable=False)
    username = db.Column(db.String(60),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    role = db.Column(db.String(60),unique=False,nullable=True)
    image = db.Column(db.Text,nullable=True)
    add_ticket = db.Column(db.Boolean,nullable=True)
    add_comment = db.Column(db.Boolean,nullable=True)
    change_status = db.Column(db.Boolean,nullable=True)
    ticket_master = db.Column(db.Boolean,nullable=True)
    technician = db.Column(db.Boolean,nullable=True)
    Report = db.Column(db.Boolean,nullable=True)
    teladmin = db.Column(db.Boolean,nullable=True)
    #OU = db.Column(db.Integer,db.ForeignKey('Organization_Unit.id'),nullable=True)
    tickets=db.relationship('Ticket',backref='owner',lazy=True) 
    comments=db.relationship('Comment',backref='owner',lazy=True) 



class Ticket(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(120),nullable=False)
    content = db.Column(db.Text,nullable=False)
    datetime = db.Column(db.String(30),nullable=False,default=str(jdatetime.date.fromgregorian(day=jdatetime.datetime.strptime( str(datetime.datetime.now()),'%Y-%m-%d %H:%M:%S.%f').day,month=jdatetime.datetime.strptime( str(datetime.datetime.now()),'%Y-%m-%d %H:%M:%S.%f').month,year=jdatetime.datetime.strptime( str(datetime.datetime.now()),'%Y-%m-%d %H:%M:%S.%f').year))+' '+str(datetime.datetime.now().strftime("%H:%M:%S")))
    priority = db.Column(db.String(10),nullable=False)
    status = db.Column(db.String(30),nullable=True)
    comments=db.relationship('Comment',backref='ticket',lazy=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    technician_id = db.Column(db.Integer)
    #priority_id = db.Column(db.Integer,db.ForeignKey('priority.id'),nullable=False)
    #Status_id = db.Column(db.Integer,db.ForeignKey('status.id'),nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    comment = db.Column(db.Text,nullable=True)
    datetime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.now)
    user_id = db.Column(db.Integer,db.ForeignKey('ticket.id'),nullable=False)
    ticket_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)





class Priority(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    Priority = db.Column(db.String(60),unique=True,nullable=False)


class Status(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    status = db.Column(db.String(60),unique=True,nullable=False)


class Telbook(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    fullname= db.Column(db.String(30),unique=False,nullable=False)
    tel=db.Column(db.String(30),unique=False,nullable=False)
    mob=db.Column(db.String(30),unique=False,nullable=True)
    email=db.Column(db.String(30),unique=False,nullable=True)  
    role= db.Column(db.String(30),unique=False,nullable=True)  


