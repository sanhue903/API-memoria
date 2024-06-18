from app.extensions import ma
from app.models import Student

class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student 
        load_instance = True
        include_fk = True

    