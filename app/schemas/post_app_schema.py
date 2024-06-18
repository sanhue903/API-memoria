from app.extensions import ma
from marshmallow import fields, validate

class Question(ma.Schema):
    id = fields.Str(required=True, validate=validate.Length(min=6, max=6))
    number = fields.Int(required=True)
    text = fields.Str(required=True)

class Chapter(ma.Schema):
    id = fields.Str(required=True, validate=validate.Length(min=6, max=6))
    number = fields.Int(required=True)
    name = fields.Str(required=True)
    questions = fields.List(fields.Nested(Question))

class PostAppSchema(ma.Schema):
    id = fields.Str(required=True, validate=validate.Length(min=6, max=6))
    name = fields.Str(required=True)
    chapters = fields.List(fields.Nested(Chapter))