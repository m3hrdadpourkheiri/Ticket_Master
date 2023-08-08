from flask import Flask
from flask import render_template,flash,url_for,redirect,request
from WebApp import app,db,bcrypt
from WebApp.models import User,Ticket,Comment
from WebApp.forms import RegistrationForm,LoginForm,NewTicketForm,CommentForm,StatusForm,NewUserForm,UpdateProfileForm,ChangeTechnicianForm
from flask_login import login_user,current_user,logout_user,login_remembered,login_required
from werkzeug.utils import secure_filename
import os
import base64
import hashlib
#from flask_uploads import configure_uploads,IMAGES,UploadSet





@app.route('/')
@login_required
def index():
    return render_template('dashboard.html')

path = os.path.join('static', 'Profile_image')
app.config['UPLOAD_FOLDER'] = path

#os.makedirs(path)

# app.config['UPLOAD_IMAGES_DEST'] = 'uploads/'
# images = UploadSet('images',IMAGES)
# configure_uploads(app,images)


@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fullname=form.fullname.data,username=form.username.data,password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash('کاربر با موفقییت ایجاد شد','success')
        return redirect(url_for('index'))
    else:
        return render_template('register.html',form=form)
    

@app.route('/ticket/new',methods=['GET','POST'])
@login_required
def new_ticket():
    #technicians=User.query.filter_by(technician=True)
    form = NewTicketForm()
    form.refer.choices =[(technician.id,technician.fullname) for technician in User.query.filter_by(technician=True)]
    
    if form.validate_on_submit():
        ticket = Ticket(title=form.title.data,content=form.content.data,priority=form.priority.data,owner=current_user,status='باز',technician_id=form.refer.data)
        db.session.add(ticket)
        db.session.commit()
        app.logger.info('data db saved !!!!!!!!!!!!!!!!')
        flash('تیکت با موفقییت ثبت شد','success')
        return redirect(url_for('index'))
    else:
        app.logger.info('data no saved ................')
        return render_template('new_ticket.html',form=form)
    










@app.route('/ticket/<int:ticket_id>/details',methods=['GET','POST'])
@login_required
def show_ticket(ticket_id):
    c_form = CommentForm()
    s_form=StatusForm()
    t_form=ChangeTechnicianForm()
    t_form.refer.choices =[(technician.id,technician.fullname) for technician in User.query.filter_by(technician=True)]
    #t_form.refer.choices.append('Please choose')
    ticket=Ticket.query.filter_by(id=ticket_id).first()

    if c_form.validate_on_submit():
        comment = Comment(comment=c_form.comment.data,owner=current_user,ticket=ticket)
        db.session.add(comment)
        db.session.commit()

    if s_form.validate_on_submit():
        ticket.status = s_form.status.data
        db.session.commit()
        flash('وضعییت تغییر کرد','success')

    if t_form.validate_on_submit():
        ticket.technician_id=t_form.refer.data
        db.session.commit()
        user=User.query.filter_by(id=t_form.refer.data).first()
        flash('ارجاع به '+user.fullname+' انجام شد','success')
        return redirect(url_for('all_ticket'))
        

    comments=Comment.query.filter_by(ticket=ticket)
    return render_template('ticket_details.html',ticket=ticket,c_form=c_form,s_form=s_form,t_form=t_form,comments=comments)



@app.route('/ticket/refer')
@login_required
def refers():
    tickets = Ticket.query.filter_by(technician_id=current_user.id)
    return render_template('tickets.html',tickets=tickets)





@app.route('/ticket/all',methods=['GET','POST'])
@login_required
def all_ticket():
    technicians = User.query.filter_by(technician=True)
    if current_user.ticket_master==True:
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter_by(owner=current_user),

    return render_template('tickets.html',tickets=tickets,technicians=technicians)

    
    









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

            flash('شما با موفقییت به سایت وارد شدید','success')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('اطلاعات ورود اشتباه می باشد','danger')
    return render_template('login.html',form=form)




@app.route('/user/new',methods=['GET','POST'])
#@login_required
def new_user():
    form= NewUserForm()
    users =User.query.all()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fullname=form.fullname.data,username=form.username.data,password=hashed_pass,role=form.role.data,add_ticket=form.add_ticket.data,add_comment=form.add_comment.data,change_status=form.change_status.data,ticket_master=form.ticket_master.data,technician=form.technician.data,Report=form.Report.data)
        db.session.add(user)
        db.session.commit()
        flash('کاربر با موفقییت ایجاد شد','success')
        
    return render_template('admin/users.html',users=users,form=form)




@app.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    user = current_user
    user.image=user.image.decode('utf-8')
    app.logger.info(user.image[0:100])
    if form.validate_on_submit():
        app.logger.info('profile updated !!!!!!!!!!!!!!!!')
        user.fullname=form.fullname.data
        user.username=form.username.data
        user.role=form.role.data
        
        if form.image.data:
            Image_file = request.files['image']
            #Image_file_name = secure_filename(Image_file.filename)
            #mimetype = Image_file.mimetype
            user.image = base64_bytes = base64.b64encode(Image_file.read()) 
  
        db.session.commit()
        flash('اطلاعات کاربری شما بروز رسانی شد','success')
    else:
        form.fullname.data=user.fullname
        form.username.data=user.username
        form.role.data=user.role
        #app.logger.info('no update !!!!!!!!!!!!!!!!')
        
    return render_template('admin/profile.html',user=current_user,form=form)


 













@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out successfully','info')
    return redirect(url_for('index'))




