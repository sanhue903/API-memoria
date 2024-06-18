from app.extensions import ma
from marshmallow import fields, validate

class LoginSchema(ma.Schema):
    email = fields.Str(required=True, validate=validate.Length(min=5, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=8, max=128))
