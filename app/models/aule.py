from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
#import random
#import string
#import datetime

from app.extensions import db#, scheduler

class Aule(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(15))

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    students: Mapped[List['AuleStudentRelationship']] = db.relationship(backref='aule', lazy=True)
    #code: Mapped[str] = mapped_column(db.String(6), nullable=True)
    
    #def generate_temporal_code(self):
    #    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
    #    while db.session.scalar(db.select(Aule).where(Aule.code == code)):
    #        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
    #    self.code = code
            
    #    return code
    
    #def reset_code(self):
    #    self.code = None
    #    db.session.commit()
        
    #def schedule_reset_code(self, app):
    #    with app.app_context():
    #        scheduler.add_job(
    #            func=self.reset_code,
    #            trigger='date',
    #            #TODO cambiar a delta de 2 horas
    #            run_date=datetime.datetime.now() + datetime.timedelta(minutes=10),
    #            id=f'reset_code_{self.id}'
    #        )
    
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
    
    def __repr__(self):
        return f'<Aule {self.id}: {self.name}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
        }