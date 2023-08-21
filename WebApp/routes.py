from flask import Flask
from flask import render_template,flash,url_for,redirect,request
from WebApp import app,db,bcrypt
from WebApp.models import User,Ticket,Comment,Telbook
from WebApp.forms import RegistrationForm,LoginForm,NewTicketForm,CommentForm,StatusForm,NewUserForm,UpdateProfileForm,ChangeTechnicianForm,NewTelForm
from flask_login import login_user,current_user,logout_user,login_remembered,login_required
import base64
import json
from config import language


with open('Ticket_App/Language_Pack/{}.json'.format(language),encoding='utf-8') as json_data:
    language_data=json.load(json_data)






@app.route('/')
@login_required
def index():
    if current_user.image:
        current_user.image=current_user.image.decode('utf-8')
    return render_template('dashboard.html',labels=language_data)



@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fullname=form.fullname.data,username=form.username.data,password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(language_data['Message_createUserSuccess'],'success')
        return redirect(url_for('index'))
    else:
        return render_template('register.html',form=form,labels=language_data)
    

@app.route('/ticket/new',methods=['GET','POST'])
@login_required
def new_ticket():
    if current_user.image:
        current_user.image=current_user.image.decode('utf-8')
    #technicians=User.query.filter_by(technician=True)
    form = NewTicketForm()
    form.refer.choices =[(technician.id,technician.fullname) for technician in User.query.filter_by(technician=True)]
    
    if form.validate_on_submit():
        ticket = Ticket(title=form.title.data,content=form.content.data,priority=form.priority.data,owner=current_user,status='باز',technician_id=form.refer.data)
        db.session.add(ticket)
        db.session.commit()
        flash(language_data['Message_TicketAddedSuccess'],'success')
        return redirect(url_for('index'))
    else:
        return render_template('new_ticket.html',form=form,labels=language_data)
    


@app.route('/ticket/<int:ticket_id>/details',methods=['GET','POST'])
@login_required
def show_ticket(ticket_id):
    if current_user.image:
        current_user.image=current_user.image.decode('utf-8')
    c_form = CommentForm()
    s_form=StatusForm()
    t_form=ChangeTechnicianForm()
    t_form.refer.choices =[(technician.id,technician.fullname) for technician in User.query.filter_by(technician=True)]
    ticket=Ticket.query.filter_by(id=ticket_id).first()

    if c_form.validate_on_submit():
        comment = Comment(comment=c_form.comment.data,owner=current_user,ticket=ticket)
        db.session.add(comment)
        db.session.commit()

    if s_form.validate_on_submit():
        ticket.status = s_form.status.data
        db.session.commit()
        flash(language_data['Message_StatusChanged'],'success')

    if t_form.validate_on_submit():
        ticket.technician_id=t_form.refer.data
        db.session.commit()
        user=User.query.filter_by(id=t_form.refer.data).first()
        flash(language_data['Message_ReferedSuccess'],'success')
        return redirect(url_for('all_ticket'))

    comments=Comment.query.filter_by(ticket=ticket)
    return render_template('ticket_details.html',ticket=ticket,c_form=c_form,s_form=s_form,t_form=t_form,comments=comments,labels=language_data)



@app.route('/ticket/refer')
@login_required
def refers():
    if current_user.image:
        current_user.image=current_user.image.decode('utf-8')
    tickets = Ticket.query.filter_by(technician_id=current_user.id)
    return render_template('tickets.html',tickets=tickets,labels=language_data)


@app.route('/ticket/all',methods=['GET','POST'])
@login_required
def all_ticket():
    if current_user.image:
        current_user.image=current_user.image.decode('utf-8')
    technicians = User.query.filter_by(technician=True)
    if current_user.ticket_master==True:
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter_by(owner=current_user)

    


    return render_template('tickets.html',tickets=tickets,technicians=technicians,labels=language_data)

    

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')

            #MESSAGE=str(language_data.Message_YouLogedinSuccess)
            #app.logger.warning(language_data[Message_YouLogedinSuccess])
            flash(language_data['Message_YouLogedinSuccess'],'success')
            return redirect(next_page if next_page else url_for('index'))
        else:
            #MESSAGE=str(language_data.Message_LoginFailed)
            #app.logger.warning(language_data[Message_YouLogedinSuccess])
            flash(language_data['Message_LoginFailed'],'danger')
    return render_template('login.html',form=form,labels=language_data)


@app.route('/user/new',methods=['GET','POST'])
#@login_required
def new_user():
    if current_user.image:
        current_user.image=current_user.image.decode('utf-8')
    form= NewUserForm()
    users =User.query.all()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fullname=form.fullname.data,username=form.username.data,password=hashed_pass,role=form.role.data,add_ticket=form.add_ticket.data,add_comment=form.add_comment.data,change_status=form.change_status.data,ticket_master=form.ticket_master.data,technician=form.technician.data,Report=form.Report.data)
        db.session.add(user)
        db.session.commit()
        flash(language_data['Message_UserCreatedSuccess'],'success')
        
    return render_template('admin/users.html',users=users,form=form,labels=language_data)




@app.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    user = current_user
    if form.validate_on_submit():
        user.fullname=form.fullname.data
        user.username=form.username.data
        user.role=form.role.data
        
        if form.image.data:
            Image_file = request.files['image']
            user.image = base64_bytes = base64.b64encode(Image_file.read()) 
  
        db.session.commit()
        flash(language_data['Message_UpdateProfileSuccess'],'success')
    else:
        form.fullname.data=user.fullname
        form.username.data=user.username
        form.role.data=user.role

    if user.image:
        user.image=user.image.decode('utf-8')

    return render_template('admin/profile.html',user=current_user,form=form,labels=language_data)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(language_data['Message_LogoutSuccess'],'info')
    return redirect(url_for('index'))





@app.route('/telbook')
def telbook():
    if current_user.image:
        current_user.image=current_user.image.decode('utf-8')
    telbook = Telbook.query.all()
    return render_template('telbook/telbook.html',telbook=telbook,labels=language_data)

@app.route('/new_tel',methods=['GET','POST'])
def new_tel():
    if current_user.image:
        current_user.image=current_user.image.decode('utf-8')
    form = NewTelForm()
    if form.validate_on_submit():
        tel = Telbook(fullname=form.fullname.data,tel=form.tel.data,mob=form.mob.data,email=form.email.data,role=form.role.data)
        db.session.add(tel)
        db.session.commit()
        return redirect(url_for('telbook'))
    return render_template('telbook/newtel.html',form=form,labels=language_data)

@app.route('/tel/<id>/delete')
def delete_tel(id):
    if current_user.image:
        current_user.image=current_user.image.decode('utf-8')
    tel = Telbook.query.filter_by(id=id).first()
    db.session.delete(tel)
    db.session.commit()
    return redirect(url_for('telbook'))

@app.route('/tel/<id>/edit',methods=['GET','POST'])
def edit_tel(id):
    if current_user.image:
        current_user.image=current_user.image.decode('utf-8')
    form = NewTelForm()
    tel = Telbook.query.filter_by(id=id).first()
    if form.validate_on_submit():
        tel.fullname=form.fullname.data
        tel.tel=form.tel.data
        tel.mob=form.mob.data
        tel.email=form.email.data
        tel.role=form.role.data
        db.session.commit()
        return redirect(url_for('telbook'))
    else:
        form.fullname.data=tel.fullname
        form.tel.data=tel.tel
        form.mob.data=tel.mob
        form.email.data=tel.email
        form.role.data=tel.role

    return render_template('telbook/edittel.html',form=form,labels=language_data)


