import time
import telepot
from telepot.loop import MessageLoop
from pprint import pprint

# bot = teleport.Bot('TOKEN')
# bot = telepot.Bot('780588064:AAGhpNay8KI5KOUSk4jRaQqMY9BahAoUfHs')
bot = telepot.Bot('801340996:AAHuXOl2XhK7wxXInSltxmWRAMfPkBfDaJE')

def handle(msg):
	pprint(msg)

MessageLoop(bot, handle).run_as_thread()
print('Listening ...')

while 1:
	time.sleep(1)
