from app.extensions import ma
from marshmallow import fields, validate


class InnerScoreSchema(ma.Schema):
    answer = fields.Str(required=True)
    seconds = fields.Float(required=True)
    is_correct = fields.Boolean(required=True)
    question_id = fields.Str(required=True, validate=validate.Length(min=6, max=6))

class ChapterSchema(ma.Schema):
    id = fields.Str(required=True, validate=validate.Length(min=6, max=6))
    scores = fields.List(fields.Nested(InnerScoreSchema), required=True)

class PostScoreSchema(ma.Schema):
    chapter = fields.Nested(ChapterSchema, required=True)
    
    