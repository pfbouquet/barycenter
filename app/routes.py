from datetime import timedelta

from flask import render_template, url_for, request
from flask_login import current_user, login_required, login_user
from werkzeug.utils import redirect

from app import app, db
from app.forms import RegistrationForm, GroupCreationForm
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
        user = User(
            username=form.username.data,
            email=form.email.data,
            address_1=form.address_1.data,
            address_2=form.address_2.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True, duration=timedelta(days=90))
        return redirect(url_for('groups'))

    return render_template('signin.html', form=form)


@app.route('/groups', methods=['GET', 'POST'])
@login_required
def groups():

    if request.method == 'POST':
        if 'group_name' in request.form:
            group = Group(name=get_post_result('group_name'), creator=current_user.username)
            db.session.add(group)
            member = Member(user_id=current_user.id, group_id=group.id)
            db.session.add(member)
            db.session.commit()
            return redirect(url_for('group', group_id=group.id))

    form = GroupCreationForm()
    groups = Group.query.join(Member).filter(Member.user_id == current_user.id).all()
    subscribe_id = request.args.get('subscribe')
    if subscribe_id:
        if subscribe_id not in [group_id for group_id in Member.query.filter_by(current_user.username).all()]:
            subscribe = Group.query.filter_by(id=subscribe_id).first()
            return render_template('groups.html', groups=groups, subscribe=subscribe, form=form)

    return render_template('groups.html', groups=groups, form=form)


@app.route('/group/<group_id>', methods=['GET', 'POST'])
@login_required
def group(group_id):
    group = Group.query.filter_by(id=group_id).first()
    members = db.session.query(User).join(Member).join(Group).filter(Group.id == group_id).all()
    return render_template('group.html', group=group, members=members)


@app.route('/result/<group_id>', methods=['POST'])
@login_required
def result(group_id):
    return render_template('result.html', group_id)
