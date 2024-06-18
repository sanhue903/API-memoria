from app.extensions import ma
from app.models import Score
from marshmallow import fields, validate

class InnerScoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Score
        load_instance = True
        include_fk = True
        exclude = ['id', 'question_id']

class QuestionSchema(ma.Schema):
    question = fields.Str(required=True, validate=validate.Length(equal=6))
    scores = fields.List(fields.Nested(InnerScoreSchema))

class ChapterSchema(ma.Schema):
    chapter = fields.Str(required=True, validate=validate.Length(equal=6))
    questions = fields.List(fields.Nested(QuestionSchema))

class GetScoreSchema(ma.Schema):
    results = fields.List(fields.Nested(ChapterSchema))