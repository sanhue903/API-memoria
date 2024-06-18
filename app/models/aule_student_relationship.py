from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db

class AuleStudentRelationship(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    aule_id: Mapped[int] = mapped_column(ForeignKey('aule.id'))
    student_id: Mapped[int] = mapped_column(ForeignKey('student.id'))

    def __init__(self, aule_id, student_id):
        self.aule_id = aule_id
        self.student_id = student_id

    def __repr__(self):
        return f'<AuleStudentRelationship {self.id}: {self.aule_id} - {self.student_id}>'

    def serialize(self):
        return {
            'id': self.id,
            'aule_id': self.aule_id,
            'student_id': self.student_id,
        }