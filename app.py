from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
import os
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Instantiate db
# db = SQLAlchemy(app)

from views import *
# from models import User, UrlSchema

if __name__ == '__main__':
    app.run()