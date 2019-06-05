from datetime import timedelta

from flask import render_template, url_for, request
from flask_login import current_user, login_required, login_user
from werkzeug.utils import redirect

from app import app, db
from app.forms import RegistrationForm
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


@app.route('/signin', methods=['GET', 'POST'])
def signin():

    if current_user.is_authenticated:
        return redirect(url_for('groups'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True, duration=timedelta(days=90))
        return redirect(url_for('groups'))

    return render_template('signin.html', form=form)


@app.route('/groups', methods=['GET', 'POST'])
@login_required
def groups():
    return render_template('groups.html')


@app.route('/group/<group_id>', methods=['GET', 'POST'])
@login_required
def group(group_id):
    return render_template('group.html', group_id)


@app.route('/result/<group_id>', methods=['POST'])
@login_required
def result(group_id):
    return render_template('result.html', group_id)


@app.route('/subscribe/<group_id>', methods=['GET', 'POST'])
def subscribe(group_id):
    return render_template('subscribe.html', group_id)
