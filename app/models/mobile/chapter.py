from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db

class Chapter(db.Model):
    id: Mapped[str] = mapped_column(db.String(6), primary_key=True)
    name: Mapped[str] = mapped_column()
    number: Mapped[int] 

    app_id: Mapped[str] = mapped_column(db.String(6), ForeignKey('application.id'))
    
    questions: Mapped[List['Question']] = db.relationship(backref='chapter', lazy=True)
    
    def __init__(self, id, app_id, number, name):
        self.id = id
        self.app_id = app_id
        self.number = number
        self.name = name
        
    def __repr__(self):
        return f'<Chapter {self.id}: {self.name}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'app_id': self.app_id
        }