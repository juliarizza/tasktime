# -*- coding: utf-8 -*-
from werkzeug.security import generate_password_hash, \
    check_password_hash
from random import choice
import string

def random_password(length=8, chars=string.letters + string.digits):
	## do not generate the most safest password in the world
	## but they are enough for temporary passwords
	## feel free to modify in your way
	## code from: http://code.activestate.com/recipes/59873-random-password-generation/
    return ''.join([choice(chars) for i in range(length)])

def set_password(password):
    return generate_password_hash(password)

def check_password(pw_hash, password):
    return check_password_hash(pw_hash, password)