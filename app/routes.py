from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request, abort
from app import app, db
from app.forms import LoginForm, RegistrationForm, FindUserForm, SendMessageForm
from app.models import User, Conversation, Conversation_users, Messages
from datetime import datetime



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = FindUserForm()
    if form.validate_on_submit():
        searched_user = form.username.data
        return redirect(url_for('search', searched_users=searched_user))
    return render_template('index.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<id>')
@login_required
def user(id):
    user = User.query.filter_by(id=id).first_or_404()
    my_conv = Conversation_users.query.filter_by(user_id=id).all()
    my_convs = []
    for c in my_conv:
        my_convs.append(Conversation.query.filter_by(id=c.conversation_id).first())
    my_conv_id = []
    for c in my_conv:
        my_conv_id.append(c.conversation_id)
    my_conv_s = Conversation_users.query.filter(Conversation_users.conversation_id.in_(my_conv_id)).all()
    for c in my_conv_s:
        if c.user_id != current_user.id:
            c.__dict__['chat_name'] = User.query.filter_by(id=c.user_id).first().username
    return render_template('user.html', user=user, conv=my_conv_s)


@app.route('/search/<searched_users>', methods=['GET', 'POST'])
def search(searched_users):
    form = FindUserForm()
    searched = User.query.filter(User.username.contains(searched_users)).order_by(User.username).all()
    if form.validate_on_submit():
        searched_user = form.username.data
        return redirect(url_for('search', searched_users=searched_user))
    return render_template('search.html', form=form, users=searched)


@app.route('/send_message/', methods=['GET', 'POST'])
def send_message():
    user_id = request.form['user_id']
    user = User.query.filter_by(id=user_id).first()
    conv1 = Conversation_users.query.filter_by(user_id=current_user.id).all()
    conv2 = Conversation_users.query.filter_by(user_id=user.id).all()
    conv = None
    i = 0
    for c1 in conv1:
        for c2 in conv2:
            if c1.conversation_id == c2.conversation_id:
                conv = c2
                print(c2.id)
                return redirect(url_for('conversation', id=conv.conversation_id))
    conv = Conversation(name=current_user.username + '-->' + user.username, type='secure')
    db.session.add(conv)
    db.session.commit()
    conv = Conversation.query.filter_by(name=current_user.username + '-->' + user.username).first()
    conv1 = Conversation_users(user_id=current_user.id, conversation_id=conv.id, read=False)
    conv2 = Conversation_users(user_id=user.id, conversation_id=conv.id, read=False)
    db.session.add_all([conv1, conv2])
    db.session.commit()
    print('e')
    return redirect(url_for('conversation', id=conv.id))


@app.route('/conversation/<id>', methods=['GET', 'POST'])
def conversation(id):
    form = SendMessageForm()
    conversation = Conversation.query.filter_by(id=id).first()
    conv_users = Conversation_users.query.filter_by(conversation_id=id).all()
    user = None
    for c in conv_users:
        if c.user_id != current_user.id:
            user = User.query.filter_by(id=c.user_id).first()
    if conversation == None:
        abort(404)
    messages = Messages.query.filter_by(conversation_id=conversation.id).all()
    if form.validate_on_submit():
        message = Messages(conversation_id=id, user_id=current_user.id, text=form.text.data, datetime=datetime.utcnow())
        db.session.add(message)
        db.session.commit()
        conv = Conversation.query.filter_by(id=id).first()
        conv.last_message_datetime = datetime.utcnow()
        db.session.commit()
        return redirect(request.referrer)
    return render_template('conversation.html', form=form, conv=conversation, messages=messages, user=user)


