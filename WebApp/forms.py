from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,TextAreaField,SelectField,FileField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from WebApp.models import User
from config import language
import json


with open('Ticket_App/Language_Pack/{}.json'.format(language),encoding='utf-8') as json_data:
    language_data=json.load(json_data)




class RegistrationForm(FlaskForm):
    fullname = StringField(language_data['RegistrationForm_Fullname'],validators=[DataRequired(), Length(min=4,max=25,message='نام کاربری باید بین 4 تا 25 کاراکتر باشد')])
    username = StringField(language_data['RegistrationForm_Username'],validators=[DataRequired()])
    password = PasswordField(language_data['RegistrationForm_Password'],validators=[DataRequired(),Length(min=8,max=25,message='کلمه عبور باید بین 8 تا 25 کاراکتر باشد')])
    confirm_password = PasswordField(language_data['RegistrationForm_ConfirmPassword'],validators=[DataRequired(),EqualTo('password',message='تایید کلمه عبور و کلمه عبور باید یکسان باشند')])

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('این نام کاربری قبلا استفاده شده است')
        
        
    """def validate_email(self,email):
        user=Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is exist. Email must be uniq')"""



class NewUserForm(FlaskForm):
    fullname = StringField(language_data['NewUserForm_Fullname'],validators=[DataRequired(), Length(min=4,max=25,message='نام کاربری باید بین 4 تا 25 کاراکتر باشد')])
    username = StringField(language_data['NewUserForm_Username'],validators=[DataRequired()])
    password = PasswordField(language_data['NewUserForm_Password'],validators=[DataRequired(),Length(min=8,max=25,message='کلمه عبور باید بین 8 تا 25 کاراکتر باشد')])
    confirm_password = PasswordField(language_data['NewUserForm_ConfirmPassword'],validators=[DataRequired(),EqualTo('password',message='تایید کلمه عبور و کلمه عبور باید یکسان باشند')])
    Unit = SelectField(language_data['NewUserForm_OrganizationUnit'])
    role = StringField(language_data['NewUserForm_Role'])
    #admin = BooleanField('دسترسی مدیریتی')
    add_ticket = BooleanField(language_data['NewUserForm_AddTicketPermission'])
    add_comment = BooleanField(language_data['NewUserForm_AddCommentPermission'])
    change_status = BooleanField(language_data['NewUserForm_ChangeStatusPermission'])
    ticket_master = BooleanField(language_data['NewUserForm_TicketMaster'])
    technician = BooleanField(language_data['NewUserForm_Technesian'])
    Report = BooleanField(language_data['NewUserForm_ReportPermission'])


    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('این نام کاربری قبلا استفاده شده است')




class UpdateProfileForm(FlaskForm):
    fullname = StringField(language_data['UpdateProfileForm_Fullname'],validators=[DataRequired(), Length(min=4,max=25,message='نام کاربری باید بین 4 تا 25 کاراکتر باشد')])
    username = StringField(language_data['UpdateProfileForm_Username'],validators=[DataRequired()])
    role = StringField(language_data['UpdateProfileForm_Role'])
    image = FileField(language_data['UpdateProfileForm_Image'])



class LoginForm(FlaskForm):
    username = StringField(language_data['LogiForm_Username'],validators=[DataRequired()])
    password = PasswordField(language_data['LogiForm_Password'],validators=[DataRequired()])
    remember = BooleanField(language_data['LogiForm_RememberMe'])
    


class NewTicketForm(FlaskForm):
    title=StringField(language_data['NewTicketForm_Title'],validators=[DataRequired(),Length(max=120,message='Title max char 120')])
    content=TextAreaField(language_data['NewTicketForm_Content'],validators=[DataRequired()])
    priority = SelectField(language_data['NewTicketForm_Priority'],choices=[('پایین','پایین'), ('متوسط','متوسط'), ('بالا','بالا'),('بحرانی','بحرانی')])
    refer = SelectField(language_data['NewTicketForm_Refer'])

class StatusForm(FlaskForm):
    status = SelectField(language_data['StatusForm_Status'],choices=[('باز','باز'), ('در حال انجام','در حال انجام'), ('درحال پیگیری','در حال پیگیری'),('معلق','معلق'),('بسته','بسته')])


class ChangeTechnicianForm(FlaskForm):
    refer = SelectField(language_data['ChangeTechnicianForm_Refer'])


class CommentForm(FlaskForm):
    comment=TextAreaField(language_data['CommentForm_Comment'],validators=[DataRequired()])


class NewTelForm(FlaskForm):
    fullname=StringField(language_data['NewTelForm_Fullname'],validators=[DataRequired(),Length(min=3,max=30,message='مقدار نام و نام خانوادگی باید بین 3 تا 30 کاراکتر باشد')])
    tel=StringField(language_data['NewTelForm_Tel'],validators=[DataRequired(),Length(min=3,max=30,message='شماره تلفن باید بین 3 تا 30 رقم باشد')])
    mob=StringField(language_data['NewTelForm_Mob'],validators=[Length(min=3,max=30,message='شماره موبایل باید بین 3 تا 30 رقم باشد')])
    email=StringField(language_data['NewTelForm_Email'],validators=[Length(min=3,max=30,message='ایمیل باید بین 3 تا 30 کاراکتر باشد')])
    role=StringField(language_data['NewTelForm_Role'],validators=[Length(min=3,max=30,message='واحد سازمانی باید بین 3 تا 30 کاراکتر باشد')])

    