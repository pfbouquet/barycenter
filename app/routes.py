from datetime import timedelta

import yaml
from flask import render_template, url_for, request, session
from flask_login import current_user, login_required, login_user
from werkzeug.utils import redirect

from app import app, db
from app.forms import RegistrationForm, GroupCreationForm
from app.models import User, Group, Member
from lib import matching
from lib.generate_dynamic_map import generate_html_map
from lib.geo_encode import address_to_geopoint
from lib.gif import get_random_gif_url
from lib.mail import MailSender, send_to_group
from lib.tools import get_database_uri


def get_post_result(key):
    return dict(request.form)[key]


@app.login_manager.unauthorized_handler
def unauthorized_handler():
    if request.args.get('subscribe'):
        session['subscribe'] = request.args['subscribe']
    return redirect(url_for('login'))


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
        if 'new_group_name' in request.form:
            group = Group(name=get_post_result('new_group_name'), creator=current_user.username)
            db.session.add(group)
            member = Member(user_id=current_user.id, group_id=group.id)
            db.session.add(member)
            db.session.commit()
            return redirect(url_for('group', group_id=group.id))
        if 'accept_group' in request.form:
            member = Member(user_id=current_user.id, group_id=request.form['accept_group'])
            db.session.add(member)
            db.session.commit()
            if session.get('subscribe'):
                session.pop('subscribe')
            return redirect(url_for('group', group_id=request.form['accept_group']))
        if 'refuse_group' in request.form:
            if session.get('subscribe'):
                session.pop('subscribe')
            return redirect(url_for('groups'))

    form = GroupCreationForm()
    groups = Group.query.join(Member).filter(Member.user_id == current_user.id).all()
    subscribe_id = request.args.get('subscribe') or session.get('subscribe')
    if subscribe_id:
        if subscribe_id not in [member.group_id for member in Member.query.filter_by(user_id=current_user.id).all()]:
            subscribe = Group.query.filter_by(id=subscribe_id).first()
            return render_template('groups.html', groups=groups, subscribe=subscribe, form=form)

    return render_template('groups.html', groups=groups, form=form)


@app.route('/group/<group_id>', methods=['GET', 'POST'])
@login_required
def group(group_id):

    if request.method == 'POST':
        if 'leave_group' in request.form:
            Member.query.filter_by(user_id=current_user.id, group_id=request.form['leave_group']).delete()
            db.session.commit()
            return redirect(url_for('groups'))

    if not db.session.query(Member.id).filter_by(group_id=group_id, user_id=current_user.id).all():
        return redirect(url_for('groups'))

    group = Group.query.filter_by(id=group_id).first()
    members = db.session.query(User).join(Member).join(Group).filter(Group.id == group_id).all()
    return render_template('group.html', group=group, members=members)


@app.route('/search/<group_id>', methods=['GET', 'POST'])
@login_required
def search(group_id):

    if request.method == 'POST':
        if 'search' in request.form:
            # GET RECIPIENTS
            session['recipients'] = [int(id) for id in request.form.getlist('recipient')]
            recipients = db.session.query(User.address_1, User.address_2) \
                .filter(User.id.in_(session['recipients'])).all()
            recipients_enriched = []
            for recipient_tuple in recipients:
                recipients_enriched.extend(map(address_to_geopoint, recipient_tuple))
            # GET BEST PLACES
            credentials = yaml.safe_load(open('conf/credentials.yaml', 'r'))
            isochrones, best_places = matching.match_bars(recipients_enriched, get_database_uri(**credentials['db']), limit=3)
            session['results'] = best_places
            # GENERATE MAP
            map_html_path = 'app/templates/map.html'
            names = db.session.query(User.username).filter(User.id.in_(session['recipients']))
            addresses = []
            for name in names:
                addresses.extend([f'{name[0]} home', f'{name[0]} work'])
            generate_html_map(
                destination=map_html_path,
                dict_isochrones=isochrones.poi_isochrone_builder,
                array_lon_lat_users=recipients_enriched,
                array_popup_users=addresses,
                array_lon_lat_bars=[(bar['longitude'], bar['latitude']) for bar in best_places],
                array_popup_bars=[bar['name'] for bar in best_places]
            )
            return render_template('result.html', results=best_places)

        if 'bar_choice' in request.form:
            recipients = db.session.query(User.username, User.email).filter(User.id.in_(session['recipients'])).all()
            group_name = db.session.query(Group.name).filter_by(id=group_id).first()[0]
            group_details = {
                'group_name': group_name,
                'users': [{'user_name': username, 'email': email} for username, email in recipients],
            }
            place_details = session['results'][int(request.form['bar_choice'])]
            credentials = yaml.safe_load(open('conf/credentials.yaml', 'r'))
            sender = MailSender(**credentials['mailsender'])
            gif_url = get_random_gif_url(term='cheers', giphy_credentials=credentials['giphy'])
            with open('app/templates/text_mail.html', 'r') as f:
                send_to_group(sender, f.read(), group_details, place_details)
            return render_template('confirm.html', group_name=group_name, gif_url=gif_url)

    group = Group.query.filter_by(id=group_id).first()
    members = db.session.query(User).join(Member).join(Group).filter(Group.id == group_id).all()
    return render_template('search.html', group=group, members=members)


@app.route('/folium_map')
def folium_map():
    return render_template('map.html')
