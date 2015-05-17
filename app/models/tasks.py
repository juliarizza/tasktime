# -*- coding: utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
from flask.ext.mail import Message
from app import mail, config_info, db
from app.models.dbs import Ticket, Contract, User
import datetime
import logging

logging.basicConfig()

scheduler = BackgroundScheduler()
now = datetime.datetime.now()

def check_all_users():
	users = User.query.filter_by(category='client').all()
	for user in users:
		print user
		tickets = Ticket.query.filter_by(client=user.id).all()
		worked_hours = datetime.timedelta(days=0, hours=0, minutes=0, seconds=0)
		for ticket in tickets:
			worked_hours += ticket.worked_hours
		print worked_hours
		contract = Contract.query.filter_by(client=user.id).first()
		hours, remainder = divmod(contract.available_hours.seconds, 3600)
		per_80 = hours*0.8
		if (worked_hours >= datetime.timedelta(hours=per_80)) and \
			(user.notified_80 == False):
			msg = Message("Atention! You only have a few hours left on %s" % config_info.trade_name,
				sender = app.config['DEFAULT_MAIL_SENDER'],
            	recipients = [app.config['DEFAULT_MAIL_SENDER'], user.email])
			msg.body = "Hello %s, You used %s of the hours you had available on %s. Take care!" % \
				(user.name, per_80, config_info.trade_name)
			mail.send(msg)
			user.notified_80 = True
			db.session.commit()
		elif (worked_hours >= contract.available_hours) and \
			(user.notified_100 == False):
			msg = Message("Atention! You reached the maximum hours limit on %s" % config_info.trade_name,
			sender = app.config['DEFAULT_MAIL_SENDER'],
			recipients = [app.config['DEFAULT_MAIL_SENDER'], user.email])
			msg.body = "Hello %s, You used all of your available hours on %s. From here and on you will be billed for extra hours." % \
				(user.name, config_info.trade_name)
			mail.send(msg)
			user.notified_100 = True
			db.session.commit()
		print 'finish'

def zero_to_all():
	if now.day == 1:
		users = User.query.filter_by(category='client').all()
		for user in users:
			contract = Contract.query.filter_by(client=user.id).first()
			if contract.used_hours < contract.total_hours:
				hours_left = contract.total_hours - contract.used_hours
			else:
				hours_left = 0
			contract.accumulated_hours = hours_left
			contract.used_hours = datetime.timedelta(days=0, hours=0, minutes=0, seconds=0)
			user.notified_100 = False
			user.notified_80 = False
			db.session.commit()

check_all = scheduler.add_job(check_all_users, 'interval', minutes=1)
zero_all = scheduler.add_job(zero_to_all, 'interval', 
	hours=24,
	start_date=datetime.datetime(year=now.year, month=now.month, day=1, hour=0, minute=0, second=1))
scheduler.start()