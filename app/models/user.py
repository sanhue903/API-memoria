import uuid
from typing import List
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db

class User(db.Model):
    id:         Mapped[uuid.UUID] = mapped_column(primary_key=True)
    email:      Mapped[str] = mapped_column(db.String(50), unique=True)
    password:   Mapped[str] = mapped_column()
    is_admin:   Mapped[bool] = mapped_column(db.Boolean, default=False)
    
    aules: Mapped[List['Aule']] = db.relationship(backref='user', lazy=True)
    
    def __init__(self, email, password):
        self.id = uuid.uuid4()
        self.email = email
        self.set_password(password)
        
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def serialize(self):
        return {
            'email': self.email,
        }