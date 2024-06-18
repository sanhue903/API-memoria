from flask import Flask
from flask_cors import CORS
from config import Config, DevelopmentConfig

from app.extensions import *

def create_app(config_class: Config= DevelopmentConfig):
    app = Flask(__name__)
    config = config_class()
    print(config.__class__.__name__)
    app.config.from_object(config)
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
    if type(config) == DevelopmentConfig:
        print("SWAGGER_URL: ", config_class.SWAGGER_URL)
        app.register_blueprint(config_class.SWAGGER_BLUEPRINT, url_prefix=config_class.SWAGGER_URL)
        print("tamos")

    return app

def create_database():
    from app.models import User, Student, Aule, Application, Chapter, Question, Score, AuleStudentRelationship
    
    db.create_all() 