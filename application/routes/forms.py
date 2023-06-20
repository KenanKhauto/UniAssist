from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.custom import user_rep

class RegistrationForm(FlaskForm):
    """
    Form for user registration.

    Attributes:
        username (StringField): Field for entering the username.
        email (StringField): Field for entering the email.
        password (PasswordField): Field for entering the password.
        confirm_password (PasswordField): Field for confirming the password.
        submit (SubmitField): Button for submitting the form.
    """

    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm your Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")
    
    def validate_username(self, username):
        """
        Custom validation to check if the username already exists in the database.

        Args:
            username (StringField): The username to be validated.

        Raises:
            ValidationError: Raised if the username already exists in the database.
        """
        user = user_rep.find_user_by_username(username.data)
        if user:
            raise ValidationError("That username is taken. Please choose a different one")
        
    def validate_email(self, email):
        """
        Custom validation to check if the email already exists in the database.

        Args:
            email (StringField): The email to be validated.

        Raises:
            ValidationError: Raised if the email already exists in the database.
        """
        email = user_rep.find_user_by_email(email.data)
        if email:
            raise ValidationError("That email is taken. Please choose a different one")


class LoginForm(FlaskForm):
    """
    Form for user login.

    Attributes:
        email (StringField): Field for entering the email.
        password (PasswordField): Field for entering the password.
        remember (BooleanField): Checkbox for remembering the user's login session.
        submit (SubmitField): Button for submitting the form.
    """

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me") # Just to make the user stays logged in
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = user_rep.find_user_by_username(username.data)
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = user_rep.find_user_by_email(email.data)
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')