from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,TextAreaField,SelectField,FileField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from WebApp.models import User





class RegistrationForm(FlaskForm):
    fullname = StringField('نام و نام خانوادگی',validators=[DataRequired(), Length(min=4,max=25,message='نام کاربری باید بین 4 تا 25 کاراکتر باشد')])
    username = StringField('نام کاربری',validators=[DataRequired()])
    password = PasswordField('کلمه عبور',validators=[DataRequired(),Length(min=8,max=25,message='کلمه عبور باید بین 8 تا 25 کاراکتر باشد')])
    confirm_password = PasswordField('تایید کلمه عبور',validators=[DataRequired(),EqualTo('password',message='تایید کلمه عبور و کلمه عبور باید یکسان باشند')])

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('این نام کاربری قبلا استفاده شده است')
        
        
    """def validate_email(self,email):
        user=Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is exist. Email must be uniq')"""



class NewUserForm(FlaskForm):
    fullname = StringField('نام و نام خانوادگی',validators=[DataRequired(), Length(min=4,max=25,message='نام کاربری باید بین 4 تا 25 کاراکتر باشد')])
    username = StringField('نام کاربری',validators=[DataRequired()])
    password = PasswordField('کلمه عبور',validators=[DataRequired(),Length(min=8,max=25,message='کلمه عبور باید بین 8 تا 25 کاراکتر باشد')])
    confirm_password = PasswordField('تایید کلمه عبور',validators=[DataRequired(),EqualTo('password',message='تایید کلمه عبور و کلمه عبور باید یکسان باشند')])
    Unit = SelectField('واحد سازمانی')
    role = StringField('سمت سازمانی')
    #admin = BooleanField('دسترسی مدیریتی')
    add_ticket = BooleanField('دسترسی ثبت تیکت جدید')
    add_comment = BooleanField('دسترسی اضافه کردن یاداشت به تیکت ها')
    change_status = BooleanField('دسترسی تغییر وضعییت تیکت ها')
    ticket_master = BooleanField('دسترسی تیکت مستر')
    technician = BooleanField('تکنسین')
    Report = BooleanField('دسترسی به گزارشات')


    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('این نام کاربری قبلا استفاده شده است')




class UpdateProfileForm(FlaskForm):
    fullname = StringField('نام و نام خانوادگی',validators=[DataRequired(), Length(min=4,max=25,message='نام کاربری باید بین 4 تا 25 کاراکتر باشد')])
    username = StringField('نام کاربری',validators=[DataRequired()])
    role = StringField('سمت سازمانی')
    image = FileField('تصویر پروفایل')



class LoginForm(FlaskForm):
    username = StringField('نام کاربری',validators=[DataRequired()])
    password = PasswordField('کلمه عبور',validators=[DataRequired()])
    remember = BooleanField('مرا بخاطر بسپار')
    


class NewTicketForm(FlaskForm):
    title=StringField('عنوان',validators=[DataRequired(),Length(max=120,message='Title max char 120')])
    content=TextAreaField('محتوای پیام',validators=[DataRequired()])
    priority = SelectField('اولوییت',choices=[('پایین','پایین'), ('متوسط','متوسط'), ('بالا','بالا'),('بحرانی','بحرانی')])
    refer = SelectField('کارشناس')

class StatusForm(FlaskForm):
    status = SelectField('وضعیت تیکت',choices=[('باز','باز'), ('در حال انجام','در حال انجام'), ('درحال پیگیری','در حال پیگیری'),('معلق','معلق'),('بسته','بسته')])


class ChangeTechnicianForm(FlaskForm):
    refer = SelectField('ارجاع به')


class CommentForm(FlaskForm):
    comment=TextAreaField('یاداشت',validators=[DataRequired()])


class NewTelForm(FlaskForm):
    fullname=StringField('نام و نام خانوادگی',validators=[DataRequired(),Length(min=3,max=30,message='مقدار نام و نام خانوادگی باید بین 3 تا 30 کاراکتر باشد')])
    tel=StringField('شماره تلفن',validators=[DataRequired(),Length(min=3,max=30,message='شماره تلفن باید بین 3 تا 30 رقم باشد')])
    mob=StringField('شماره موبایل',validators=[Length(min=3,max=30,message='شماره موبایل باید بین 3 تا 30 رقم باشد')])
    email=StringField('ایمیل',validators=[Length(min=3,max=30,message='ایمیل باید بین 3 تا 30 کاراکتر باشد')])
    role=StringField('واحد سازمانی',validators=[Length(min=3,max=30,message='واحد سازمانی باید بین 3 تا 30 کاراکتر باشد')])

    