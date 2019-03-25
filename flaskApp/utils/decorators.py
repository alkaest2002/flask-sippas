from functools import wraps
from threading import Thread
from flask import redirect, url_for
from flask_login import current_user

def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                return redirect(url_for('users.unauthorized'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def asynchronous(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
