from flask import Blueprint, redirect, url_for, flash, render_template, request
from projectmngt import db, bcrypt
from flask_login import current_user, logout_user, login_user,login_required
from projectmngt.users.forms import *

users = Blueprint('users', __name__)

@users.route('/register',methods=['GET','POST'])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(full_name = form.full_name.data, email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash('User added successful', 'success')
        return redirect(url_for('users.Login'))

    return render_template('register.html', title = 'Register', form=form)

@users.route('/login', methods=['GET','POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check your email and password', 'danger')
    return render_template('login.html', title = 'Login', form=form)


@users.route('/logout')
def Logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account')
@login_required
def Account():
    return render_template('account.html', title = 'Account')