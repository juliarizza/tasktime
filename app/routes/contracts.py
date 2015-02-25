# -*- coding: utf-8 -*-
from flask import render_template, flash, \
    redirect, url_for
from flask.ext.sqlalchemy import Pagination
from app import app, db
from app.models.dbs import Contract
from app.models.forms import NewContract

@app.route('/contracts', defaults={'page':1})
@app.route('/contracts/<int:page>')
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
def new_contract():
    form = NewContract()
    if form.validate_on_submit():
        entry = Contract(**form.data)
        db.session.add(entry)
        db.session.commit()
        flash("New contract added: %s" %\
            (form.title.data), 'success')
        return redirect(url_for('show_contracts'))
    return render_template('contracts/new_contract.html',
                            form=form,
                            action="new_contract",
                            title="New Contract")

@app.route('/edit_contract/<int:id>', methods=['GET', 'POST'])
def edit_contract(id):
    contract = Contract.query.get(id)
    form = NewContract(obj=contract)
    if form.validate_on_submit():
        Contract.query.filter(Contract.id==id).update(
            form.data
            )
        db.session.commit()
        flash('Contract edited: %s' %
            (form.title.data), 'success')
        return redirect(url_for('show_contracts'))
    return render_template('contracts/new_contract.html',
                            title='Edit Contract',
                            action="edit_contract",
                            id=id,
                            form=form)

@app.route('/delete_contract/<int:id>')
def delete_contract(id):
    contract = Contract.query.get(id)
    db.session.delete(contract)
    db.session.commit()
    flash('Contract removed: %s' % contract.title, 'info')
    return redirect(url_for('show_contracts'))
