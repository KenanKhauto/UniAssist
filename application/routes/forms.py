
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.custom import user_rep

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
    confirm_password = PasswordField("Confirm your Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")
    

    ## Make sure that the field does not exist in database
    ## if it exists, raise error
    def validate_username(self, username):
        user = user_rep.find_user_by_username(username.data)
        if user:
            raise ValidationError("That username is taken. Please choose a different one")
        
    def validate_email(self, email):
        email = user_rep.find_user_by_email(email.data)
        if email:
            raise ValidationError("That email is taken. Please choose a different one")


class LoginForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me") # Just to make the user stays logged 
    submit = SubmitField("Login")