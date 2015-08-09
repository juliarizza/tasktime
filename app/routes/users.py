# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect,\
    url_for, g, abort
from flask.ext.sqlalchemy import Pagination
from flask.ext.mail import Message
from flask.ext.login import login_required,\
    login_user, logout_user, current_user
from flask.ext.babel import gettext
from app import app, db, login_manager,\
    config_info, mail
from app.models.dbs import User
from app.models.forms import RegisterUser, LoginForm,\
    ChangePassword
from app.models.global_functions import random_password,\
    requires_roles

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

@app.route('/team', defaults={'page':1})
@app.route('/team/<int:page>')
@requires_roles('admin')
def show_users(page):
    users = User.query.filter((User.category=='employee') \
        | (User.category=='admin')).all()
    per_page = 10
    items = users[(page-1)*per_page:per_page*page]
    pagination = Pagination(users, page, per_page,\
                            len(users), items)
    return render_template('users/users.html',
                            title=gettext('Users'),
                            users=items,
                            pagination=pagination)

@app.route('/user/<int:id>')
@requires_roles('admin')
def show_user(id):
    user = User.query.get_or_404(id)
    return render_template('users/user.html',
                            title=gettext('User'),
                            user=user)

@app.route('/register_user', methods=['GET', 'POST'])
@requires_roles('admin')
def register_user():
    form = RegisterUser()
    if form.validate_on_submit():
        password = random_password()
        entry = User(category='employee', **form.data)
        entry.set_password(password)
        db.session.add(entry)
        db.session.commit()
        flash(gettext('New user on list: %s' %\
            (form.name.data)), 'success')
        msg = Message(gettext("You were registered on %s" % config_info.trade_name),
            sender = app.config['DEFAULT_MAIL_SENDER'],
            recipients = [form.email.data])
        msg.html = gettext("""
                    You were registered in the ticketing system of %(company)s 
                    as a team member. To open new tickets and access your tickets info 
                    use this data.<br>
                    <b>Email:</b> %(email)s <br>
                    <b>Password:</b> %(password)s <br>
                    This password was generated automatically. For your safety, change 
                    your password in your first access.
                   """ % {'company': config_info.trade_name, 'email': form.email.data,
                        'password': password})
        mail.send(msg)
        return redirect(url_for('show_user', id=entry.id))
    return render_template('users/register_user.html', 
                           title=gettext('Register User'),
                           action='register_user',
                           form=form)

@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
@requires_roles('admin')
def edit_user(id):
    user = User.query.get_or_404(id)
    form = RegisterUser(obj=user)
    if form.validate_on_submit():
        User.query.filter_by(id=id).update(
            form.data
            )
        db.session.commit()
        flash(gettext('User edited: %s' % form.name.data), 'success')
        return redirect(url_for('show_users'))
    return render_template('users/register_user.html',
                            title=gettext('Edit User'),
                            action='edit_user',
                            id=id,
                            form=form)

@app.route('/delete_user/<int:id>')
@requires_roles('admin')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash(gettext('User removed: %s' % user.name), 'info')
    return redirect(url_for('show_users'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('show_tickets'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            authorized = user.check_password(form.password.data)
            if authorized:
                login_user(user, remember=form.remember_me.data)
                flash(gettext("Logged in!"), "success")
                return redirect(url_for('index'))
        flash(gettext("Invalid login!"), "danger")
        return redirect(url_for("login"))
    return render_template('users/login.html', 
                           title=gettext('Sign In'),
                           form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(gettext("Logged out!"), "info")
    return redirect(url_for('index'))

@app.route('/change_password/<int:id>',
    methods=['POST', 'GET'])
@login_required
def change_password(id):
    user = User.query.get_or_404(id)

    form = ChangePassword()
    if form.validate_on_submit():
        if (form.new_password.data == form.new_password_2.data) \
            and user.check_password(form.old_password.data):
            user.set_password(form.new_password.data)
            db.session.commit()
            flash(gettext("Password changed!"), "success")
            return redirect(url_for('index'))
        else:
            flash(gettext("Data do not match!"), "danger")
            return redirect(url_for('change_password', id=id))

    return render_template('users/change_password.html',
                            title=gettext("Change Password"),
                            form=form)

@app.route('/reset_password/<int:id>',
    methods=['POST', 'GET'])
def reset_password(id):
    user = User.query.get_or_404(id)

    form = ChangePassword()
    del form.old_password
    if form.validate_on_submit():
        if form.new_password.data == form.new_password_2.data:
            user.set_password(form.new_password.data)
            db.session.commit()
            flash(gettext("Password reseted!"), "success")
            return redirect(url_for('index'))
        else:
            flash(gettext("Passwords does not match!"), "danger")
            return redirect(url_for('reset_password', id=id))

    return render_template('users/change_password.html',
                            title=gettext("Reset Password"),
                            form=form)

@app.route('/profile')
@login_required
def profile():
    if current_user.get_category() == 'client':
        current_user.role = gettext('Client')
    return render_template('users/user.html',
                            title=gettext("Profile"),
                            user=current_user)

@app.route('/preset_users')
def preset_users():
    if User.query.count() == 0:
        admin_user = User(name="Admin", email="admin@admin.com", category="admin")
        admin_user.set_password("admin")
        employee_user = User(name="Employee", email="employee@employee.com", category="employee")
        employee_user.set_password("employee")
        client_user = User(name="Client", email="client@client.com", category="client")
        client_user.set_password("client")
        db.session.add(admin_user)
        db.session.add(employee_user)
        db.session.add(client_user)
        db.session.commit()
        flash(gettext("Preset users created!"), "info")
    return redirect(url_for('index'))
