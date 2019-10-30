############# import for Telepot <BEGIN> #############
import datetime
import telepot
from telepot.loop import MessageLoop
############# import for Telepot <BEGIN> #############

############# Telegram bot <BEGIN> #######################################
def action(msg):
    #global chat_id
    chat_id = msg['chat']['id']
    text = msg['text']
    print ('Received: %s' % text)
    telegram_bot.sendMessage (chat_id, message)
telegram_bot = telepot.Bot('801340996:AAHuXOl2XhK7wxXInSltxmWRAMfPkBfDaJE')
#print (telegram_bot.getMe())
#MessageLoop(telegram_bot, action).run_as_thread()
############# Telegram bot <END> #######################################

############# Telegram bot <BEGIN> #######################################
while 1:
	# Because the int(<str>) function cannot convert an empty string to integer,
	# it shows "invalid literal for int() with base 10" if <str> is empty
	# = "** WARNING! FIRE MAY OCCUR! **\n"
	# Send message to telegram if flame occurs
	try:
		message = ("** WARNING! FIRE MAY OCCUR! **\n")
		telegram_bot.sendMessage (137763952, message)
	except ValueError:
		pass
	############# Telegram bot <END> #########################################