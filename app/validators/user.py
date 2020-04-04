"""
User validation schemas.
"""
from marshmallow import pre_load, Schema, validates_schema, ValidationError
from marshmallow.fields import Bool, Email, Str
from marshmallow.validate import Length


class UserCreateSchema(Schema):
    email = Email(required=True)
    password = Str(required=True, validate=Length(min=8))
    confirm_password = Str(required=True, validate=Length(min=8))
    first_name = Str(required=True, validate=Length(max=100))
    last_name = Str(required=True, validate=Length(max=100))

    @pre_load
    def make_data(self, data, **kwargs):
        data['email'] = data.pop('email').lower().strip()
        data['first_name'] = data.pop('first_name').strip()
        data['last_name'] = data.pop('last_name').strip()
        return data

    @validates_schema
    def validates_password_confirmation(self, data, **kwargs):
        if data['password'] != data['confirm_password']:
            raise ValidationError(confirm_password='Passwords didn\'t match')
