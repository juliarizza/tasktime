# -*- coding: utf-8 -*-
from app import app
import os

basedir = os.path.abspath(os.path.dirname(__file__))

## DATABASES
SQLALCHEMY_DATABASE_URI = "postgresql://localhost:5432/tasktime"

## WTFORMS
WTF_CSRF_ENABLED = True

## APP
SECRET_KEY = '19akdcsmjxn&*2304&qn,q'
DEBUG = True

## AVAILABLE LANGUAGES
LANGUAGES = {
    'en': 'English',
    'pt': 'Português (Brasil)'
}
