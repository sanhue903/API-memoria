from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

from app.extensions import db


class Student(db.Model):
    id:   Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50))
    age:  Mapped[int]
    session: Mapped[int] = mapped_column(default=0)
    
    app_id: Mapped[str] = mapped_column(ForeignKey('application.id'), nullable=False)

    aules: Mapped[List['AuleStudentRelationship']] = db.relationship(backref='student', lazy=True)
    scores: Mapped[List['Score']] = db.relationship(backref='student', lazy=True)    
    
    def __init__(self,app_id, name, age):
        self.name = name    
        self.age = age
        self.app_id = app_id
        
    def __repr__(self):
        return f'<Student {self.id}: {self.name}>'
        