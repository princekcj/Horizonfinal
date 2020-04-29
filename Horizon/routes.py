from flask import render_template, url_for, flash, redirect, request
from Horizon.horizonforms import RegistrationForm, LoginForm, TransferForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from urllib.request import urlopen
from Horizon import db, app, bcrypt, mail
from Horizon.models import User, Transaction
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

posts = [
    {
        'author': 'Horizon Pay',
        'title': 'Borderless Transfer',
        'content': 'Send Ghanaian Cedis to any African country, Fast and Fee - Less',
        'date_posted': 'March 21, 2020'
    },
    {
        'author': 'Horizon Pay',
        'title': 'African Currency Exchange',
        'content': 'Check and Change Your Cedis Into Any African Currency',
        'date_posted': 'April 21, 2018'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/exchangerates", methods=['GET', 'POST'])
def exchangerates():
    with urlopen('https://api.currconv.com/api/v7/convert?q=GHS_RWF,GHS_DZD,GHS_NGN,GHS_SLL,GHS_XOF,GHS_XAF,GHS_CDF,GHS_EGP,GHS_ZAR,GHS_SOS&compact=ultra&apiKey=ad753aeed7974a11ad350212d37f5fca') as conn:
        raw_data = conn.read()
        import json
        encoding = conn.info().get_content_charset('utf8')
        conversions = json.loads(raw_data.decode(encoding))
        import ast
        conversions = str(conversions)
        conversions = ast.literal_eval(conversions)
        globals().update(conversions)
    #currency_conversion('GHS_DZD')
    #output = currency_conversion('GHS_DZD').exchange
    conversion = float(1)
    if request.method == 'POST':
        conversion = request.form['conversion']
        conversion = float(conversion)
    output = round((GHS_DZD)*(conversion), 2)
    output_1 = round((GHS_RWF)*(conversion), 2)
    output_2 = round((GHS_NGN)*(conversion), 2)
    output_3 = round((GHS_SLL)*(conversion), 2)
    output_4 = round((GHS_XOF)*(conversion), 2)
    output_5 = round((GHS_XAF)*(conversion), 2)
    output_6 = round((GHS_EGP)*(conversion), 2)
    output_7 = round((GHS_SOS)*(conversion), 2)
    output_8 = round((GHS_ZAR)*(conversion), 2)
    output_9 = round((GHS_CDF)*(conversion), 2)
    return render_template('exchangerates.html', title='Exchange Rates', output=output, output_1=output_1, output_2=output_2, output_3=output_3, output_4 =output_4, output_5=output_5, output_6=output_6, output_7=output_7, output_8=output_8, output_9=output_9)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You may log in now', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/transfermoney", methods=['GET', 'POST'])
@login_required
def transfermoney():
    form = TransferForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        if bcrypt.check_password_hash(user.password, form.password.data):
            transactions = Transaction(username=current_user.username, receiving_username=form.receiving_username.data, amount=form.amount.data, currency=form.currency.data, Transactor=current_user)
            db.session.add(transactions)
            db.session.commit()
            flash('Transfer Successful')
            return redirect(url_for('transfermoney'))
        else:
            flash('Transfer Unsuccessful. Please check password', 'danger')
    return render_template('transfermoney.html', title='Transfer Money', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}
    
    If you did not make request then simply ignore this email and no changes will be made
    '''


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template ('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('The password has been updated! You may log in now', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form= form)
