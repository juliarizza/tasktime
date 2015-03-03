# -*- coding: utf-8 -*-
from werkzeug.security import check_password_hash
from flask.ext.login import current_user
from random import choice
from functools import wraps
import string

def random_password(length=8, chars=string.letters + string.digits):
	## do not generate the most safest password in the world
	## but they are enough for temporary passwords
	## feel free to modify in your way
	## code from: http://code.activestate.com/recipes/59873-random-password-generation/
    return ''.join([choice(chars) for i in range(length)])

def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.get_category() not in roles:
                return error_response()
            return f(*args, **kwargs)
        return wrapped
    return wrapper