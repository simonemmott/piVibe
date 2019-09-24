from flask import Flask
from piVibe import Vibrator
from config import Config
from flask_bootstrap import Bootstrap
from logger import configure_logging

configure_logging()


app = Flask(__name__)
app.config.from_object(Config)

vibe = Vibrator(18)

from app.api import bp as api_bp
app.register_blueprint(api_bp)

bootstrap = Bootstrap(app)

from app import routes