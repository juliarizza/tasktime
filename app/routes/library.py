# -*- coding: utf-8 -*-
from flask import render_template, flash, \
    redirect, url_for
from flask.ext.sqlalchemy import Pagination
from flask.ext.babel import gettext
from app import app, db
from app.models.dbs import Article, User
from app.models.forms import NewArticle
from app.models.global_functions import requires_roles
from flask.ext.login import current_user

@app.route('/library', defaults={'page':1})
@app.route('/library/<int:page>')
def show_articles(page):
    articles = Article.query.all()
    per_page = 10
    items = articles[(page-1)*per_page:per_page*page]
    pagination = Pagination(articles, page, per_page,\
                            len(articles), items)
    return render_template('library/library.html',
                            articles=items,
                            pagination=pagination)

@app.route('/article/<int:id>')
def show_article(id):
    article = Article.query.get_or_404(id)
    return render_template('library/article.html',
                            article=article)

@app.route('/new_article', methods=['GET', 'POST'])
@requires_roles('admin', 'employee')
def new_article():
    form = NewArticle()
    ## form choices
    form.author.choices = [(a.id, a.name) for a in \
        User.query.filter((User.category=='employee') \
        | (User.category=='admin')).all()]
    form.author.default = current_user.id
    if form.validate_on_submit():
        entry = Article(**form.data)
        db.session.add(entry)
        db.session.commit()
        flash(gettext("New article added: %s" %\
            form.title.data), "success")
        return redirect(url_for('show_articles'))
    return render_template('library/new_article.html',
                            form=form,
                            action="new_article",
                            title=gettext("New Article"))


@app.route('/edit_article/<int:id>', methods=['GET', 'POST'])
@requires_roles('admin', 'employee')
def edit_article(id):
    article = Article.query.get_or_404(id)
    form = NewArticle(obj=article)
    ## form choices
    form.author.choices = [(a.id, a.name) for a in \
        User.query.filter((User.category=='employee') \
        | (User.category=='admin')).all()]
    form.author.default = current_user.id
    if form.validate_on_submit():
        Article.query.filter(Article.id==id).update(
            form.data
            )
        db.session.commit()
        flash(gettext("Article edited: %s" %\
            form.title.data), "success")
        return redirect(url_for('show_article', id=id))
    return render_template('library/new_article.html',
                            title=gettext('Edit Article'),
                            action="edit_article",
                            id=id,
                            form=form)

@app.route('/delete_article/<int:id>')
@requires_roles('admin', 'employee')
def delete_article(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash(gettext('Article removed: %s' % article.title), 'info')
    return redirect(url_for('show_articles'))
