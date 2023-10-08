from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,EmailField
from wtforms.validators import InputRequired, Length, NumberRange, Email



class RegisterForm(FlaskForm):
    """Register form"""
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(),Length(min=6, max=55)])
    email = EmailField("Email",validators=[InputRequired(),Email(), Length(max=50)] )
    first_name = StringField("First name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last name", validators=[InputRequired(), Length(max=30)])

    # EqualTo('confirm', message='Passwords must match')]


class LoginForm(FlaskForm):
    """Login form"""
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=55)])

class FeedbackForm(FlaskForm):
    """Feedback form"""
    title = StringField("Title", validators=[InputRequired(),Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])


class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank.""" 
    # ????