# -*- coding: utf-8 -*-
from flask import render_template, flash, \
    redirect, url_for
from flask.ext.sqlalchemy import Pagination
from flask.ext.login import login_required, current_user
from app import app, db
from app.models.dbs import Ticket, User, Contract
from app.models.forms import NewTicket
from app.models.global_functions import requires_roles

@app.route('/tickets', defaults={'page':1})
@app.route('/tickets/<int:page>')
@login_required
def show_tickets(page):
    if current_user.get_category() == 'client':
        tickets = Ticket.query.filter_by(client=current_user.id).all()
    elif current_user.get_category() == 'employee':
        tickets = Ticket.query.filter_by(employee=current_user.id).all()
    else:
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
    ticket = Ticket.query.get_or_404(id)
    return render_template('tickets/ticket.html',
                            title='Ticket',
                            ticket=ticket)

@app.route('/new_ticket', methods=['GET', 'POST'])
def new_ticket():
    form = NewTicket()
    ## form choices
    form.client.choices = [(c.id, c.name) for c in \
        User.query.filter_by(category='client').all()]
    form.employee.choices = [(e.id, e.name) for e in \
        User.query.filter((User.category=='employee') \
        | (User.category=='admin')).all()]
    form.contract.choices = [(c.id, c.title) for c in Contract.query.all()]
    if current_user.get_category() == 'client':
        form.client.default == current_user.id        
    else:
        form.employee.default == current_user.id
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
    ticket = Ticket.query.get_or_404(id)
    form = NewTicket(obj=ticket)
    ## form choices
    form.client.choices = [(c.id, c.name) for c in \
        User.query.filter_by(category='client').all()]
    form.employee.choices = [(e.id, e.name) for e in \
        User.query.filter((User.category=='employee') \
        | (User.category=='admin')).all()]
    form.contract.choices = [(c.id, c.title) for c in Contract.query.all()]
    if form.validate_on_submit():
        Ticket.query.filter(Ticket.id==id).update(
            form.data
            )
        db.session.commit()
        flash("Ticket edited: %s" %\
            form.title.data, "success")
        return redirect(url_for('ticket_info', id=id))
    return render_template('tickets/new_ticket.html',
                            title='Edit Ticket',
                            action="edit_ticket",
                            id=id,
                            form=form)

@app.route('/delete_ticket/<int:id>')
def delete_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket removed: %s' % ticket.title, 'info')
    return redirect(url_for('show_tickets'))