# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
from app import app, db
from app.models.forms import RegisterClient
from app.models.dbs import Client

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
        entry = Client(name=form.name.data,
                        company=form.company.data,
                        email=form.email.data,
                        address=form.address.data,
                        city=form.city.data,
                        state=form.state.data,
                        phone=form.phone.data)
        db.session.add(entry)
        db.session.commit()
        flash('New client on list: %s' %\
            (form.name.data))
        return redirect(url_for('show_clients'))
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
        client.name = form.name.data
        client.company = form.company.data
        client.email = form.email.data
        client.address = form.address.data
        client.city = form.city.data
        client.state = form.state.data
        client.phone = form.phone.data
        db.session.commit()
        flash('Client edited: %s' % form.name.data)
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
    return redirect(url_for('show_clients'))