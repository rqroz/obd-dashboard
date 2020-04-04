"""
User validation schemas.
"""
from marshmallow import Schema
from marshmallow.fields import Email, Str
from marshmallow.validate import Length


class LoginSchema(Schema):
    email = Email(required=True)
    password = Str(required=True, validate=Length(min=8))
