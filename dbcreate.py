#from WebApp.models import User,Ticket,Priority,Status,Organization_Unit,Comment
from WebApp import db
from WebApp import app

with app.app_context():
    db.drop_all()
    db.create_all()