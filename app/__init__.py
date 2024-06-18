from flask import Flask
from flask_cors import CORS
from config import Config, DevelopmentConfig, ProductionConfig

from app.extensions import *

def create_app(config_class: Config= DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    # Initialize Flask extensions here

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    #scheduler.init_app(app) 
    
    #scheduler.start()
    
    with app.app_context():
        create_database()

    # Register blueprints here
    from app.main import bp as test_bp
    app.register_blueprint(test_bp)
    
    from app.student import bp as student_bp
    app.register_blueprint(student_bp, url_prefix='/apps/<app_id>/students')
    
    from app.score import bp as score_bp
    app.register_blueprint(score_bp, url_prefix='/apps/<app_id>/students')
    
    #from app.aule import bp as aules_bp
    #app.register_blueprint(aules_bp, url_prefix='/aules')
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.application import bp as application_bp
    app.register_blueprint(application_bp, url_prefix='/apps')
    
    
    ### Swagger ###
    if config_class is DevelopmentConfig:
        app.register_blueprint(config_class.SWAGGER_BLUEPRINT, url_prefix=config_class.SWAGGER_URL)

    return app

def create_database():
    from app.models import User, Student, Aule, Application, Chapter, Question, Score, AuleStudentRelationship
    
    db.create_all() 
    
def initial_data():
    from app.models import Application, Chapter, Question
    app_id = 'BOTIKI'

    chapter_1 = Chapter('CONEMO', 1,'Conciencia Emocional', app_id)
    db.session.add(chapter_1)
    db.session.commit()
    
    question_1_1 = Question('CONEM1', 'CONEMO', '¿Como?', 1)
    db.session.add(question_1_1)
    db.session.commit()

    chapter_2 = Chapter('REGEMO', 2, 'Conciencia Emocional', app_id)
    db.session.add(chapter_2)
    db.session.commit()
    
    chapter_3 = Chapter('AUTEMO', 3,'Autonomia Emocional', app_id)
    db.session.add(chapter_3)
    db.session.commit()
    
    question_3_1_1 = Question('AUTE11', 'AUTEMO', '¿Cómo se sentia Jacinta en su primer dia de colegio?', 1)
    question_3_1_2 = Question('AUTE12', 'AUTEMO', '¿Qué hizo Jacinta al darse cuenta que cambió de color?', 2)
    question_3_1_3 = Question('AUTE13', 'AUTEMO', '¿Por qué Jacinta decidió mostrar sus colores?', 3)
    question_3_1_4 = Question('AUTE14', 'AUTEMO', '¿Por qué es importante que Jacinta siga adelante, a pesar de sentirse avergonzada?', 4)
    question_3_1_5 = Question('AUTE15', 'AUTEMO', '¿Por qué Jacinta hablaba sola frente al espejo cuando sentía que todos se reirían de ella por estar llena de colores?', 5)
    question_3_1_6 = Question('AUTE16', 'AUTEMO', '¿Qué aprendió Jacinta cuando entró a la sala de clases y vio a todos los demás llenos de color también?', 6)
    db.session.add(question_3_1_1)
    db.session.add(question_3_1_2)
    db.session.add(question_3_1_3)
    db.session.add(question_3_1_4)
    db.session.add(question_3_1_5)
    db.session.add(question_3_1_6)
    db.session.commit()
    
    
    chapter_4 = Chapter('COMEMO', 4,'Competencia Emocional', app_id)
    db.session.add(chapter_4)
    db.session.commit()
 