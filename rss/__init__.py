from flask import Flask
from flask_cors import CORS
import logging

# Create the webserver
app = Flask(
    __name__,
    static_url_path='',
    static_folder='../public'
)

# Add the configuration
app.config.from_pyfile('settings.py')
app.logger.setLevel(level=logging.INFO)


# Allow cross-domain requests
CORS(app)

from rss import routes