# -*- coding: utf-8 -*-
from flask import render_template, flash, \
    redirect, url_for
from flask.ext.sqlalchemy import Pagination
from flask.ext.login import login_required, current_user
from app import app, db
from app.models.dbs import Ticket, User, Contract
from app.models.forms import NewTicket, NewTicketClient
from app.models.global_functions import requires_roles
import datetime

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
    contract = Contract.query.filter_by(client=ticket.client).first_or_404()
    hours, remainer = divmod(ticket.worked_hours.seconds, 3600)
    minutes, seconds = divmod(remainer, 60)
    worked_hours = (hours, minutes, seconds)
    return render_template('tickets/ticket.html',
                            title='Ticket',
                            ticket=ticket,
                            contract=contract,
                            worked_hours=worked_hours)

@app.route('/new_ticket', methods=['GET', 'POST'])
def new_ticket():
    if current_user.get_category() == 'client':
        form = NewTicketClient()
    else:
        form = NewTicket()
        ## form choices
        form.client.choices = [(c.id, c.name) for c in \
            User.query.filter_by(category='client').all()]
        form.employee.choices = [(e.id, e.name) for e in \
            User.query.filter((User.category=='employee') \
            | (User.category=='admin')).all()]
    if form.validate_on_submit():
        if current_user.get_category() == 'client':
            entry = Ticket(client=current_user.id, **form.data)
        else:
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
    if current_user.get_category() == 'client':
        form = NewTicketClient(obj=ticket)
    else:
        form = NewTicket(obj=ticket)
        ## form choices
        form.client.choices = [(c.id, c.name) for c in \
            User.query.filter_by(category='client').all()]
        form.employee.choices = [(e.id, e.name) for e in \
            User.query.filter((User.category=='employee') \
            | (User.category=='admin')).all()]
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

@app.route('/start_ticket/<int:id>')
@requires_roles('admin', 'employee')
def start_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    now = datetime.datetime.now()
    if not ticket.start_time:
        Ticket.query.filter_by(id=id).update(
            {'start_time': now,
             'play_time': now,
             'status': 'on hold'}
            )
        db.session.commit()
        flash("Started!", "success")
    else:
        Ticket.query.filter_by(id=id).update(
            {'play_time': now}
            )
        db.session.commit()
        flash("Keep going! :D", "success")
    return redirect(url_for("show_tickets"))

@app.route('/pause_ticket/<int:id>')
@requires_roles('admin', 'employee')
def pause_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    contract = Contract.query.filter_by(client=ticket.client).first_or_404()
    now = datetime.datetime.now()
    hours = now-ticket.play_time
    Ticket.query.filter_by(id=id).update(
        {'pause_time': now,
         'worked_hours': ticket.worked_hours+hours}
        )
    Contract.query.filter_by(client=ticket.client).update(
        {'used_hours': contract.used_hours+hours}
        )
    db.session.commit()
    flash("Paused!", "warning")
    return redirect(url_for("show_tickets"))

@app.route('/stop_ticket/<int:id>')
@requires_roles('admin', 'employee')
def stop_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    contract = Contract.query.filter_by(client=ticket.client).first_or_404()
    now = datetime.datetime.now()
    if ticket.pause_time and ticket.pause_time > ticket.play_time:
        Ticket.query.filter_by(id=id).update(
            {'end_time': now,
            'status': 'closed'}
            )
    else:
        hours = now-ticket.play_time
        Ticket.query.filter_by(id=id).update(
            {'end_time': now,
             'worked_hours': ticket.worked_hours+hours,
             'status': 'closed'}
            )
        Contract.query.filter_by(client=ticket.client).update(
            {'used_hours': contract.used_hours+hours}
            )
    db.session.commit()
    flash("All done!", "success")
    return redirect(url_for("show_tickets"))