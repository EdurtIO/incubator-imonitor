from services.service_user import UserService
from wtforms.validators import ValidationError


class ValidatorEmailRepeat():

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if UserService().find_by_email(field.data) is not None:
            raise ValidationError('邮箱已被注册')
