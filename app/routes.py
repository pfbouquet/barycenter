from datetime import timedelta

from flask import render_template, url_for, request
from flask_login import current_user, login_required, login_user
from werkzeug.utils import redirect

from app import app
from app.models import User


def get_post_result(key):
    return dict(request.form)[key]


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('groups'))

    if request.method == 'POST':
        if 'username' in request.form:
            user = User.query.filter_by(username=get_post_result('username')).first()
            if user is None or not user.check_password(get_post_result('password')):
                return redirect(url_for('login'))
            login_user(user, remember=True, duration=timedelta(days=90))
            return redirect(url_for('groups'))

    return render_template('login.html')


@app.route('/groups', methods=['GET', 'POST'])
@login_required
def groups():
    return render_template('groups.html')
