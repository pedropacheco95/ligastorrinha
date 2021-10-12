from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from ligastorrinha.models import User , Player , Edition , League

def add_to_session():
    leagues = League.query.all()
    session['leagues'] = leagues
    return 0