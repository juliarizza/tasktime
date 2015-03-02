# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
from flask.ext.sqlalchemy import Pagination
from app import app, db, login_manager
from app.models.dbs import User
from app.models.forms import RegisterUser
from app.models.global_functions import random_password,\
    set_password

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

@app.route('/users', defaults={'page':1})
@app.route('/users/<int:page>')
def show_users(page):
    users = User.query.all()
    per_page = 10
    items = users[(page-1)*per_page:per_page*page]
    pagination = Pagination(users, page, per_page,\
                            len(users), items)
    return render_template('users/users.html',
                            title='Users',
                            users=items,
                            pagination=pagination)

@app.route('/user/<int:id>')
def show_user(id):
    user = User.query.get(id)
    return render_template('users/user.html',
                            title='User',
                            user=user)

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    form = RegisterUser()
    if form.validate_on_submit():
        password = random_password()
        pw_hash = set_password(password)
        entry = User(password=pw_hash, **form.data)
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
def edit_user(id):
    user = User.query.get(id)
    form = RegisterUser(obj=user)
    if form.validate_on_submit():
        User.query.filter(User.id==id).update(
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
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash('User removed: %s' % user.name, 'info')
    return redirect(url_for('show_users'))