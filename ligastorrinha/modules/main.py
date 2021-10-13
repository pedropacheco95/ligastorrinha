from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from ligastorrinha.models import User , Player , Edition , League

bp = Blueprint('main', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    if 'leagues' not in session.keys():
        leagues = League.query.all()
        session['leagues'] = leagues
    return render_template('index.html')
