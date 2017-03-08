from flask import Flask

import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0')
