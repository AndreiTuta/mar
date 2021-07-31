from wtforms import Form , StringField , SelectField, IntegerField, PasswordField , SubmitField , validators

class LoginForm(Form) :
    uname = StringField("Username" , validators=[
        validators.DataRequired() ,
        validators.Length(min=4 , max=20)
    ])
    password = PasswordField("Password" , validators=[
        validators.DataRequired()
    ])
    submit = SubmitField("Login")