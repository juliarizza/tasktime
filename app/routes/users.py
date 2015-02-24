# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
from app import app, db
from app.models.forms import RegisterClient
from app.models.dbs import Client
from app.models.global_functions import random_password,\
    set_password

@app.route('/clients', methods=['GET'])
def show_clients():
    clients = Client.query.all()
    return render_template('clients.html',
                            title='Clients',
                            clients=clients)

@app.route('/client/<int:id>', methods=['GET'])
def show_client(id):
    client = Client.query.get(id)
    return render_template('client.html',
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
            (form.name.data))
        return redirect(url_for('show_client', id=entry.id))
    return render_template('register_client.html', 
                           title='Register Client',
                           action='register_client',
                           id = '',
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
        flash('Client edited: %r' % form.name.data)
        return redirect(url_for('show_clients'))
    return render_template('register_client.html',
                            title='Edit Client',
                            action='edit_client',
                            id=id,
                            form=form)

@app.route('/delete/<int:id>')
def delete_client(id):
    client = Client.query.get(id)
    db.session.delete(client)
    db.session.commit()
    flash('Client removed: %r' % client.name)
    return redirect(url_for('show_clients'))