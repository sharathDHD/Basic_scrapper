from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import logging

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app import routes
    app.register_blueprint(routes.bp)

    # Set up logging
    logging.basicConfig(filename='app.log', level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')

    return app