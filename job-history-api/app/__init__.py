from flask import Flask
from app.models import db
from app.config import Config

def create_app(config_class=Config):
    '''
    Application factory pattern.
    
    Args:
        config_class: Configuration class to use
    
    Returns:
        Configured Flask application
    '''
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database with app
    db.init_app(app)
    
    # Import and register routes blueprint
    from app.routes import api
    app.register_blueprint(api)
    
    # Create tables within app context
    with app.app_context():
        db.create_all()
    
    return app
