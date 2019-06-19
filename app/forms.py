from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class RegistrationForm(FlaskForm):

    username = StringField(
        'Username', validators=[DataRequired(), Length(8, 20)], render_kw={'placeholder': 'Username'}
    )
    email = StringField(
        'Email', validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email'}
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(8, 40)], render_kw={'placeholder': 'Password'}
    )
    password2 = PasswordField(
        'Repeat password', validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder': 'Repeat password'}
    )
    address_1 = StringField(
        'Home address', validators=[DataRequired(), Length(10, 100)], render_kw={'placeholder': 'Home address'}
    )
    address_2 = StringField(
        'Work address', validators=[DataRequired(), Length(10, 100)], render_kw={'placeholder': 'Work address'}
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already used. Please enter a new one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class GroupCreationForm(FlaskForm):

    new_group_name = StringField(
        'Group  name', validators=[DataRequired(), Length(5, 20)], render_kw={'placeholder': 'Group name'}
    )
    submit = SubmitField('Create group')
