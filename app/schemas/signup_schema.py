from app.extensions import ma
from marshmallow import fields, validate

class SignUpSchema(ma.Schema):
    email = fields.Email(required=True, validate=validate.Length(min=5, max=40))
    password = fields.Str(required=True, validate=validate.Length(min=8, max=128))
    confirm_password = fields.Str(required=True)