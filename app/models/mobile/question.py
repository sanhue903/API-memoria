from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db

class Question(db.Model):
    id: Mapped[str] = mapped_column(db.String(6), primary_key=True)
    text: Mapped[str] = mapped_column()
    chapter_id: Mapped[str] = mapped_column(db.String(6), ForeignKey('chapter.id'))
    number: Mapped[int] 
    
    scores: Mapped[List['Score']] = db.relationship(backref='question', lazy=True)
    
    def __init__(self, id, chapter_id, number, text):
        self.id = id
        self.text = text
        self.chapter_id = chapter_id
        self.number = number
        
    def __repr__(self):
        return f'<Question {self.id}: {self.text}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'text': self.text,
            'chapter_id': self.chapter_id
        }
    