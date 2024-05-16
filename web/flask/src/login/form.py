from wtforms import Form
from wtforms import PasswordField
from wtforms import StringField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
