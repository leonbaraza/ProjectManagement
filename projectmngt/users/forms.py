from wtforms import SubmitField, StringField, PasswordField, ValidationError
from wtforms.validators import Email, EqualTo, DataRequired
from flask_wtf import FlaskForm
from projectmngt.models import Users

class RegisterForm(FlaskForm):
    full_name = StringField('First Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Email Address', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_fullname(self, full_name):
        user = Users.query.filter_by(full_name = full_name.data).first()
        if user:
            raise ValidationError('Username already exists..')

    def validate_email(self, email):
        email = Users.query.filter_by(email = email.data).first()
        if email:
            raise ValidationError('Email already exists..')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Email Address', validators=[DataRequired()])
    submit = SubmitField('Register')

