import functools
from flask import redirect, session, url_for

class Descriptor(object):
    def __init__(self, func):
        self.func = func
    def __get__(self, inst, type=None):
        val = self.func(inst)
        setattr(inst, self.func.__name__, val)
        return val

def reify(func):
    return functools.wraps(func)(Descriptor(func))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        user = session['user']
        if not user.admin:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view