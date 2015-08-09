# -*- coding: utf-8 -*-
from flask import abort
from app import app
from werkzeug.security import check_password_hash
from flask.ext.login import current_user
from flask.ext.babel import gettext
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
    ## code from: http://flask.pocoo.org/snippets/98/
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_anonymous() and current_user.get_category() not in roles:
                return abort(401)
            return f(*args, **kwargs)
        return wrapped
    return wrapper

from datetime import datetime

@app.template_filter('friendly_time')
def friendly_time(dt, past_=gettext("ago"), 
    future_=gettext("from now"), 
    default=gettext("just now")):
    #code from: http://flask.pocoo.org/snippets/33/
    """
    Returns string representing "time since"
    or "time until" e.g.
    3 days ago, 5 hours from now etc.
    """

    now = datetime.utcnow()
    if now > dt:
        diff = now - dt
        dt_is_past = True
    else:
        diff = dt - now
        dt_is_past = False

    periods = (
        (diff.days / 365, gettext("year"), gettext("years")),
        (diff.days / 30, gettext("month"), gettext("months")),
        (diff.days / 7, gettext("week"), gettext("weeks")),
        (diff.days, gettext("day"), gettext("days")),
        (diff.seconds / 3600, gettext("hour"), gettext("hours")),
        (diff.seconds / 60, gettext("minute"), gettext("minutes")),
        (diff.seconds, gettext("second"), gettext("seconds")),
    )

    for period, singular, plural in periods:
        
        if period:
            return "%d %s %s" % (period, \
                singular if period == 1 else plural, \
                past_ if dt_is_past else future_)

    return default
