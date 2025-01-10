import telegram
import logging
from telegram.ext import Updater, CommandHandler
from telegram_bot import id_to_name, name_to_id
import time 
import math
import random

from openpyxl import Workbook
from openpyxl import load_workbook

callie_events = load_workbook('callie_events.xlsx')
events = callie_events['Events']

admin = INSERT_ID

updater = Updater(token='INSERT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
	# print("start")
	context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def send_updates(update, context):
	global admin, events, callie_events
	msg = ""
	if update.effective_chat.id != admin:
		msg = "Admins only!"
		context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
		return 

	number_of_entries = events['F1'].value
	for i in range(number_of_entries):
		update_id = events[str('A' + str(i+2))].value
		countdown_event = events[str('B' + str(i+2))].value
		days_left = events[str('C' + str(i+2))].value
		last_sent = events[str('D' + str(i+2))].value
		time_now = int(time.time())

		if math.floor(time_now/86400) - math.floor(last_sent/86400) == 0:
			# i am Lazy
			msg = "Update was sent to " + id_to_name(update_id) + " at " + str(last_sent) + ". Please wait " + str(86400 - time_now%86400) + " more seconds until the next update."
			context.bot.send_message(chat_id=admin, text=msg)
			continue

		# oh actually sending the update !!
		random_sound = ["Mrrp! ", "Woof! ", "Woof woof! ", "Mrrrrrrrr. ", "AHHHHHHHHH. Only ", "Oh no. Only ", "**dying noises** Only ", "BooOOoOOoOOo! ", "Bleh. ", "**egg rolling noises** ", "Booooop. ", "Arf! ", ""]
		thing = random_sound[random.randint(0, len(random_sound)-1)]
		end_msg = ["! That's all for today.", "! Good luck everyone, y'alls are doing great!", "! Rip", "! How eggciting.", "! Yay!", "! **eggcited egg noises", "! Kksdfjksdfd.", "! Woohoo!", ". Sexc", ". Oh.", ". Naisu", ". Unnaisu.", "!!!", "! haha"]
		thing2 = end_msg[random.randint(0, len(end_msg)-1)]
		msg = thing + str(days_left) + " more days until " + countdown_event + thing2
		context.bot.send_message(chat_id=update_id, text=msg)
		days_left -= 1 
		last_sent = time_now
		events[str('C' + str(i+2))] = days_left
		events[str('D' + str(i+2))] = last_sent
	context.bot.send_message(chat_id=admin, text="Done sending!")
	callie_events.save('callie_events.xlsx')

def new(update, context):
	global events, callie_events
	msg = ""
	try:
		new_event, days_left = update.message.text[5:].split(", ")
		days_left = int(days_left)
	except:
		msg = "Error: insufficient arguments. Format: /new <event>, <days left>"
		context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
		return
	number_of_entries = events['F1'].value
	events[str('A' + str(number_of_entries+2))] = update.effective_chat.id
	events[str('B' + str(number_of_entries+2))] = new_event
	events[str('C' + str(number_of_entries+2))] = days_left
	events[str('D' + str(number_of_entries+2))] = '0'
	number_of_entries += 1
	events['F1'] = number_of_entries
	context.bot.send_message(chat_id=update.effective_chat.id, text="Done successfully!")
	callie_events.save('callie_events.xlsx')


start_handler = CommandHandler('start', start)
new_handler = CommandHandler('new', new)
send_update_handler = CommandHandler('sendupdates', send_updates)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(new_handler)
dispatcher.add_handler(send_update_handler)

updater.start_polling()
# updater.idle()
