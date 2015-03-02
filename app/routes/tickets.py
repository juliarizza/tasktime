# -*- coding: utf-8 -*-
from flask import render_template, flash, \
    redirect, url_for
from flask.ext.sqlalchemy import Pagination
from app import app, db
from app.models.dbs import Ticket, Client, \
    User, Contract
from app.models.forms import NewTicket

@app.route('/tickets', defaults={'page':1})
@app.route('/tickets/<int:page>')
def show_tickets(page):
    tickets = Ticket.query.all()
    per_page = 10
    items = tickets[(page-1)*per_page:per_page*page]
    pagination = Pagination(tickets, page, per_page,\
                            len(tickets), items)
    return render_template('tickets/tickets.html',
                            tickets=items,
                            pagination=pagination)

@app.route('/ticket/<int:id>')
def ticket_info(id):
    ticket = Ticket.query.get(id)
    print ticket.client
    return render_template('tickets/ticket.html',
                            title='Ticket',
                            ticket=ticket)

@app.route('/new_ticket', methods=['GET', 'POST'])
def new_ticket():
    form = NewTicket()
    ## form choices
    form.client.choices = [(c.id, c.name) for c in Client.query.all()]
    form.employee.choices = [(e.id, e.name) for e in User.query.all()]
    form.contract.choices = [(c.id, c.title) for c in Contract.query.all()]
    if form.validate_on_submit():
        entry = Ticket(**form.data)
        db.session.add(entry)
        db.session.commit()
        flash("New ticket added: %s" %\
            form.title.data, "success")
        return redirect(url_for('show_tickets'))
    return render_template('tickets/new_ticket.html',
                            form=form,
                            action="new_ticket",
                            title="New Ticket")

@app.route('/edit_ticket/<int:id>', methods=['GET', 'POST'])
def edit_ticket(id):
    ticket = Ticket.query.get(id)
    form = NewTicket(obj=ticket)
    ## form choices
    form.client.choices = [(c.id, c.name) for c in Client.query.all()]
    form.employee.choices = [(e.id, e.name) for e in User.query.all()]
    form.contract.choices = [(c.id, c.title) for c in Contract.query.all()]
    if form.validate_on_submit():
        Ticket.query.filter(Ticket.id==id).update(
            form.data
            )
        db.session.commit()
        flash("Ticket edited: %s" %\
            form.title.data, "success")
        return redirect('ticket', id=id)
    return render_template('tickets/new_ticket.html',
                            title='Edit Ticket',
                            action="edit_ticket",
                            id=id,
                            form=form)

@app.route('/delete_ticket/<int:id>')
def delete_ticket(id):
    ticket = Ticket.query.get(id)
    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket removed: %s' % ticket.title, 'info')
    return redirect(url_for('show_tickets'))