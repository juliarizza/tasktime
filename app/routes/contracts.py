# -*- coding: utf-8 -*-
from flask import render_template, flash, \
    redirect, url_for
from flask.ext.sqlalchemy import Pagination
from flask.ext.babel import gettext
from app import app, db
from app.models.dbs import Contract, User
from app.models.forms import NewContract
from app.models.global_functions import requires_roles
import datetime

@app.route('/contracts', defaults={'page':1})
@app.route('/contracts/<int:page>')
@requires_roles('admin', 'employee')
def show_contracts(page):
    contracts = Contract.query.all()
    per_page = 10
    items = contracts[(page-1)*per_page:per_page*page]
    pagination = Pagination(contracts, page, per_page,\
                            len(contracts), items)
    return render_template('contracts/contracts.html',
                            contracts=items,
                            pagination=pagination)

@app.route('/new_contract', methods=['GET', 'POST'])
@requires_roles('admin')
def new_contract():
    form = NewContract()
    form.client.choices = [(c.id, c.name) for c in User.query.filter_by(category='client').all()]
    if form.validate_on_submit():
        form.total_hours.data = datetime.timedelta(hours=form.total_hours.data)
        entry = Contract(**form.data)
        db.session.add(entry)
        db.session.commit()
        flash(gettext("New contract added: %s" %\
            (form.client.data)), 'success')
        return redirect(url_for('show_contracts'))
    return render_template('contracts/new_contract.html',
                            form=form,
                            action="new_contract",
                            title=gettext("New Contract"))

@app.route('/edit_contract/<int:id>', methods=['GET', 'POST'])
@requires_roles('admin')
def edit_contract(id):
    contract = Contract.query.get_or_404(id)
    form = NewContract(obj=contract)
    form.client.choices = [(c.id, c.name) for c in Client.query.filter_by(category='client').all()]
    if form.validate_on_submit():
        form.total_hours.data = datetime.timedelta(hours=form.total_hours.data)
        Contract.query.filter(Contract.id==id).update(
            form.data
            )
        db.session.commit()
        flash(gettext('Contract edited: %s' %
            (form.client.data)), 'success')
        return redirect(url_for('show_contracts'))
    return render_template('contracts/new_contract.html',
                            title=gettext('Edit Contract'),
                            action="edit_contract",
                            id=id,
                            form=form)

@app.route('/delete_contract/<int:id>')
@requires_roles('admin')
def delete_contract(id):
    contract = Contract.query.get_or_404(id)
    db.session.delete(contract)
    db.session.commit()
    flash(gettext('Contract removed: %s' % contract.client.name), 'info')
    return redirect(url_for('show_contracts'))
