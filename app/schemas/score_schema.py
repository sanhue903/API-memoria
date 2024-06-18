from app import ma
from app.models import Score
from marshmallow import fields, validate

class ScoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Score
        load_instance = True
        include_fk = True
        exclude = ['id', 'date']
        
    