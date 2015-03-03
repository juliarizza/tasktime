# -*- coding: utf-8 -*-
from flask import render_template, g
from app import app

@app.route('/')
def index():
	return render_template('index.html',
							title='Home')