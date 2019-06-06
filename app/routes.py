from datetime import timedelta

from flask import render_template, url_for, request
from flask_login import current_user, login_required, login_user
from werkzeug.utils import redirect

from app import app, db
from app.forms import RegistrationForm
from app.models import User, Group, Member


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
    groups = Group.query.filter_by(creator=current_user.username).all()
    return render_template('groups.html', groups=groups)


@app.route('/group/<group_id>', methods=['GET', 'POST'])
@login_required
def group(group_id):
    group = Group.query.filter_by(id=group_id).all()
    if not len(group) == 1:
        return redirect(url_for('groups'))
    else:
        group = group[0]
    members = Member.query.filter_by(group_id=group.id)
    return render_template('group.html', group=group, members=members)


@app.route('/result/<group_id>', methods=['POST'])
@login_required
def result(group_id):
    return render_template('result.html', group_id)
