# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect,\
    url_for, g, abort
from flask.ext.sqlalchemy import Pagination
from flask.ext.login import login_required,\
    login_user, logout_user, current_user
from app import app, db, login_manager
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
                            title='Users',
                            users=items,
                            pagination=pagination)

@app.route('/user/<int:id>')
@requires_roles('admin')
def show_user(id):
    user = User.query.get_or_404(id)
    return render_template('users/user.html',
                            title='User',
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
        flash('New user on list: %s' %\
            (form.name.data), 'success')
        return redirect(url_for('show_user', id=entry.id))
    return render_template('users/register_user.html', 
                           title='Register User',
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
        flash('User edited: %s' % form.name.data, 'success')
        return redirect(url_for('show_users'))
    return render_template('users/register_user.html',
                            title='Edit User',
                            action='edit_user',
                            id=id,
                            form=form)

@app.route('/delete_user/<int:id>')
@requires_roles('admin')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User removed: %s' % user.name, 'info')
    return redirect(url_for('show_users'))

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            authorized = user.check_password(form.password.data)
            if authorized:
                login_user(user, remember=form.remember_me.data)
                flash("Logged in!", "success")
                return redirect(url_for('index'))
        flash("Invalid login!", "danger")
        return redirect(url_for("login"))
    return render_template('users/login.html', 
                           title='Sign In',
                           form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out!", "info")
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
            flash("Password changed!", "success")
            return redirect(url_for('index'))
        else:
            flash("Data don't match!", "danger")
            return redirect(url_for('change_password', id=id))

    return render_template('users/change_password.html',
                            title="Change Password",
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
            flash("Password reseted!", "success")
            return redirect(url_for('index'))
        else:
            flash("Passwords doesn't match!", "danger")
            return redirect(url_for('reset_password', id=id))

    return render_template('users/change_password.html',
                            title="Reset Password",
                            form=form)

@app.route('/profile')
@login_required
def profile():
    if current_user.get_category() == 'client':
        current_user.role = 'Client'
    return render_template('users/user.html',
                            title="Profile",
                            user=current_user)
