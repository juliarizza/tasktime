# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
from flask.ext.sqlalchemy import Pagination
from app import app, db
from app.models.forms import RegisterClient
from app.models.dbs import Client
from app.models.global_functions import random_password,\
    set_password

@app.route('/clients', defaults={'page':1})
@app.route('/clients/<int:page>')
def show_clients(page):
    clients = Client.query.all()
    per_page = 10
    items = clients[(page-1)*per_page:per_page*page]
    pagination = Pagination(clients, page, per_page,\
                            len(clients), items)
    return render_template('clients/clients.html',
                            title='Clients',
                            clients=items,
                            pagination=pagination)

@app.route('/client/<int:id>')
def show_client(id):
    client = Client.query.get(id)
    return render_template('clients/client.html',
                            title='Client',
                            client=client)

@app.route('/register_client', methods=['GET', 'POST'])
def register_client():
    form = RegisterClient()
    if form.validate_on_submit():
        password = random_password()
        pw_hash = set_password(password)
        entry = Client(password=pw_hash, **form.data)
        db.session.add(entry)
        db.session.commit()
        flash('New client on list: %s' %\
            (form.name.data), 'success')
        return redirect(url_for('show_client', id=entry.id))
    return render_template('clients/register_client.html', 
                           title='Register Client',
                           action='register_client',
                           form=form)

@app.route('/edit_client/<int:id>', methods=['GET', 'POST'])
def edit_client(id):
    client = Client.query.get(id)
    form = RegisterClient(obj=client)
    if form.validate_on_submit():
        Client.query.filter(Client.id==id).update(
            form.data
            )
        db.session.commit()
        flash('Client edited: %s' % form.name.data, 'success')
        return redirect(url_for('show_clients'))
    return render_template('clients/register_client.html',
                            title='Edit Client',
                            action='edit_client',
                            id=id,
                            form=form)

@app.route('/delete_client/<int:id>')
def delete_client(id):
    client = Client.query.get(id)
    db.session.delete(client)
    db.session.commit()
    flash('Client removed: %s' % client.name, 'info')
    return redirect(url_for('show_clients'))