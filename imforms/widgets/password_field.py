from wtforms import PasswordField
from wtforms.widgets.core import PasswordInput


class PasswordField(PasswordField):
    widget = PasswordInput(hide_value=False)
