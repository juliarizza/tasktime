# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.mongoalchemy import MongoAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = MongoAlchemy(app)

from app.models import dbs
from app.routes import index