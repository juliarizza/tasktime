# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
from flask.ext.sqlalchemy import Pagination
from flask.ext.mail import Message
from flask.ext.babel import gettext
from app import app, db, config_info, mail
from app.models.forms import RegisterClient
from app.models.dbs import User
from app.models.global_functions import random_password,\
    requires_roles

@app.route('/clients', defaults={'page':1})
@app.route('/clients/<int:page>')
@requires_roles('admin', 'employee')
def show_clients(page):
    clients = User.query.filter_by(category='client').all()
    per_page = 10
    items = clients[(page-1)*per_page:per_page*page]
    pagination = Pagination(clients, page, per_page,\
                            len(clients), items)
    return render_template('clients/clients.html',
                            title=gettext('Clients'),
                            clients=items,
                            pagination=pagination)

@app.route('/client/<int:id>')
@requires_roles('admin', 'employee')
def show_client(id):
    client = User.query.get_or_404(id)
    return render_template('clients/client.html',
                            title=gettext('Client'),
                            client=client)

@app.route('/register_client', methods=['GET', 'POST'])
@requires_roles('admin', 'employee')
def register_client():
    form = RegisterClient()
    if form.validate_on_submit():
        password = random_password()
        entry = User(category='client', **form.data)
        entry.set_password(password)
        db.session.add(entry)
        db.session.commit()
        flash(gettext('New client on list: %s' %\
            (form.name.data), 'success'))
        msg = Message(gettext("You were registered on %s" % config_info.trade_name,
            sender = app.config['DEFAULT_MAIL_SENDER'],
            recipients = [form.email.data]))
        msg.html = gettext("""
                    You were registered in the ticketing system of %(company)s 
                    as a client. To open new tickets and access your tickets info 
                    use this data.<br>
                    <b>Email:</b> %(email)s <br>
                    <b>Password:</b> %(password)s <br>
                    This password was generated automatically. For your safety, change 
                    your password in your first access.
                   """ % {'company': config_info.trade_name, 'email': form.email.data,
                        'password': password})
        mail.send(msg)
        return redirect(url_for('show_client', id=entry.id))
    return render_template('clients/register_client.html', 
                           title=gettext('Register Client'),
                           action='register_client',
                           form=form)

@app.route('/edit_client/<int:id>', methods=['GET', 'POST'])
@requires_roles('admin', 'employee')
def edit_client(id):
    client = User.query.get_or_404(id)
    form = RegisterClient(obj=client)
    if form.validate_on_submit():
        User.query.filter_by(id=id).update(
            form.data
            )
        db.session.commit()
        flash(gettext('Client edited: %s' % form.name.data), 'success')
        return redirect(url_for('show_clients'))
    return render_template('clients/register_client.html',
                            title=gettext('Edit Client'),
                            action='edit_client',
                            id=id,
                            form=form)

@app.route('/delete_client/<int:id>')
@requires_roles('admin', 'employee')
def delete_client(id):
    client = User.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    flash(gettext('Client removed: %s' % client.name), 'info')
    return redirect(url_for('show_clients'))