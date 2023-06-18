from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

### For MrNaji the idiot ###

# you know that in html you have to create forms (look them up if do not know them)
# This here is just a shortcut for us in order to spare us some time with html and css
# so that we do not have to worry about the restrictions that we need to add
# to a login or a registraion form
# And since this is a very common process, you can always find packages to
# to work with them, and in our project we use flask_wtf, you can see the imports above


class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")



class LoginForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me") # Just to make the user stays logged in for some minutes after leaving the browser
    submit = SubmitField("Sign Up")