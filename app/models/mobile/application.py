from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db

class Application(db.Model):
    id: Mapped[str] = mapped_column(db.String(6), primary_key=True)
    name: Mapped[str] = mapped_column()


    chapters: Mapped[List['Chapter']] = db.relationship(backref='application', lazy=True)
    
    def __init__(self, id, name):
        self.id = id
        self.name = name
 
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def __repr__(self):
        return f'<App {self.id}: {self.name}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }