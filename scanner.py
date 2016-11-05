from unidenbct15x import *
import time
import os

PORT = '/dev/ttyUSB0'
SPEED = 115200
DEBUG = False #True

def menu(line1, line2, line3, frequency='', alertstatus=False, \
	ccstatus=False, strength='', vol='', sql=''):

	spacerwith = 30

	spacer1 = " " * (spacerwith - len(line1))
	spacer2 = " " * (spacerwith - len(line2))
	spacer3 = " " * (spacerwith - len(line3))
	spacer4 = " " * (spacerwith - len(frequency))

	display = """
  +--------------------------------+
  | {0} {3}|
  | {1} {4}|
  | {2} {5}|
  | {6} {7}|
  +--------------------------------+
  """.format(line1, line2, line3, spacer1, spacer2, spacer3, \
  	frequency, spacer4)

	if alertstatus == True:
		alertled = "*"
 	else:
 		alertled = " "

	if ccstatus == True:
 		ccled = "*"
	else:
		ccled = " "

 	leds = """| Alert ({0})        CC ({1})        |
  +--------------------------------+
  """.format(alertled, ccled)
  
  	if strength != '':
		vol = vol.strip()
		sql = sql.strip()

	 	spacer4 = " " * (13 - len(str(strength)))
	 	spacer5 = " " * (22 - len(str(vol)))
	 	spacer6 = " " * (21 - len(str(sql)))

		levels = """| Signal Strength: {0} {3}|
  | Volume: {1} {4}|
  | Squelch: {2} {5}|
  +--------------------------------+
  """.format(strength, vol, sql, spacer4, spacer5, spacer6)
	else:
		levels = ''

	controls = """| P PRI          < Turn Knob >   |
  | W WX   |1|2|3|      *  *       |
  | G GPS  |4|5|6|   *        *    |
  | M MENU |7|8|9|  *  Push =  *   |
  | L L/O  |.|0|E|  *     F    *   |
  | V VOL Push       *        *    |
  | Q SQL Push          *  *       |
  | S Scan/Search                  |
  | H Hold                         |
  | Z Radio Info                   |
  +--------------------------------+
  | Modes                          |
  | P = Press, L = Long Press      |
  | H = Hold, R = Release          |
  +--------------------------------+
  | B Set Volume                   |
  | D Set Squelch                  |
  +--------------------------------+
"""

	fullmenu = display + leds + levels + controls

	return fullmenu


def commandloop(ser, button):

	# set time out
	# funtion 2 sec
	# system 3 sec

	if button == 'F':
		timeout = 2
	elif button == '<' or '>':
		timeout = 3

	line1, line2, line3 = scanner.collectscreen(ser)
	print menu(line1, line2, line3)

	print "You have ten seconds to answer!"

	i, o, e = select.select( [sys.stdin], [], [], 10 )

	if (i):
            print "You said", sys.stdin.readline().strip()
	else:
            print "You said nothing!"

	time.sleep(timeout)

##############
# Main Routines
##############
ser = scanner.openserial(PORT, SPEED)

try:
	while True:
		line1, line2, line3, alertstatus, ccstatus, frequency = \
		scanner.collectscreen(ser)
		strength = scanner.signalstrength(ser)
		vol =  scanner.volume(ser)[1]
		sql =  scanner.squelch(ser)[1]

		os.system('clear')

		print menu(line1, line2, line3, frequency=frequency, \
			alertstatus=alertstatus, ccstatus=ccstatus, \
			strength=strength, vol=vol, sql=sql)
		time.sleep(1)

except KeyboardInterrupt:
	print "W: interrupt received, stopping..."
	ser.close()

finally:
	ser.close()


