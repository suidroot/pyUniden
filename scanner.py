#!/usr/bin/which python3
# Uniden BCT15X Scanner user interface
#
# Author: Ben Mason
# Version: 0.1
#
import time
import os
import sys
import unidenbct15x

__author__ = "Ben Mason"
__copyright__ = "Copyright 2017"
__version__ = "0.1"
__email__ = "locutus@the-collective.net"
__status__ = "Development"

PORT = '/dev/ttyUSB0'
SPEED = 115200
DEBUG = False #True

# def menu(line1, line2, line3, frequency='', alertstatus=False, \
#     ccstatus=False, strength='', vol='', sql=''):
def menu(screendata, strength='', vol='', sql=''):

    line1 = screendata['line1']
    line2 = screendata['line2']
    line3 = screendata['line3']
    if 'frequency' in screendata.keys():
        frequency = screendata['frequency']
    else:
        frequency = ''

    if 'alertstatus' in screendata.keys():
        alertstatus = screendata['alertstatus']
    else:
        alertstatus = False

    if 'ccstatus' in screendata.keys():
        ccstatus = screendata['ccstatus']
    else:
        ccstatus = False

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

    if alertstatus:
        alertled = "*"
    else:
        alertled = " "

    if ccstatus:
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


def commandloop(scanner, button):

    # set time out
    # funtion 2 sec
    # system 3 sec

    if button == 'F':
        timeout = 2
    elif button == '<' or '>':
        timeout = 3

    screenoutput = scanner.collectscreen()
    print menu(screenoutput['line1'], screenoutput['line2'], screenoutput['line3'])

    print "You have ten seconds to answer!"

    i, o, e = select.select([sys.stdin], [], [], 10)

    if (i):
        "You said", sys.stdin.readline().strip()
    else:
        print "You said nothing!"

    time.sleep(timeout)

def main():
    ##############
    # Main Routines
    ##############
    scanner = unidenbct15x.Unidenbct15x()
    scanner.openserial(PORT, SPEED)

    try:
        while True:
            # line1, line2, line3, alertstatus, ccstatus, frequency = \
            screenoutput = scanner.collectscreen()
            strength = scanner.signalstrength()
            vol = scanner.volume()[1]
            sql = scanner.squelch()[1]

            os.system('clear')

            print menu(screenoutput, strength=strength, vol=vol, sql=sql)
            # print menu(line1, line2, line3, frequency=frequency, \
            #     alertstatus=alertstatus, ccstatus=ccstatus, \
            #     strength=strength, vol=vol, sql=sql)
            time.sleep(1)

    except KeyboardInterrupt:
        print "W: interrupt received, stopping..."
        scanner.closeserial()

    finally:
        scanner.closeserial()

if __name__ == "__main__":
    # args = initargs()
    main()
