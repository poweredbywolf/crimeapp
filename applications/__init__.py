from flask import Flask
from os import environ
import config

configuration = config.Config()
app = Flask(__name__)


from applications import routes