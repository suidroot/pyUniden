#!/usr/bin/which python3
# Library for controlling a Uniden BCT15X scanner
#
# Author: Ben Mason
# Version: 0.1
#
import serial

DEBUG = False #True

__author__ = "Ben Mason"
__copyright__ = "Copyright 2017"
__version__ = "0.1"
__email__ = "locutus@the-collective.net"
__status__ = "Development"

class Unidenbct15x(object):
    """ Uniden BCT15X Object """
    ser = None

    def ___init___(self):
        """ Init """
        pass

    def openserial(self, port, speed):
        """ Open Serial Port """
        self.ser = serial.Serial(port, baudrate=speed, timeout=1, xonxoff=False, rtscts=False, dsrdtr=False)
        #print(self.ser.name)         # check which port was really used
        # return ser

    def closeserial(self):
        """ Close Serial Conenction """
        self.ser.close()

    def sendcommand(self, command, returnlength):
        """ Write to Serial Port and return output """
        self.ser.write(command + '\r')     # write a string
        self.ser.flush()
        line = self.ser.read(returnlength)

        if DEBUG:
            print line

        if 'ERR' in line:
            print "INVALID COMMAND!!!!"

        return line

    def checkok(self, radiooutput):
        """ Verify that OK was received back """
        radiooutput = radiooutput.split(',')[1]
        radiooutput = radiooutput.strip()

        if radiooutput != 'OK':
            print "ERROR"
            status = False
        else:
            status = True

        return status

    def getscreen(self):
        """ Collect Data shown on scanner Screen """
        line = self.sendcommand('STS', 136)
        displayarray = line.split(',')

        if DEBUG:
            print displayarray

        if displayarray[1] == '011000':
            # Home Screen
            # ['STS',
            # '011000',                 DISP_FORM    1
            # '                ',         L1_CHAR        2
            # '',                         L1_MODE        3
            # 'PortlandCity    ',         L2_CHAR        4
            # '',                         L2_MODE        5
            # 'H   ID SEARC \x81  ',     L3_CHAR        6
            # '',                         L3_MODE        7
            # ' 852.7875       ',         L4_CHAR        8
            # '',                         L4_MODE        9
            # 'S0:----------   ',         L5_CHAR        10
            # '',                         L5_MODE        11
            # '              WX',        L6_CHAR        12
            # '',                         L6_MODE        13
            # '1',                         SQL         14
            # '1',                         MUT         15
            # '0',                         RSV            16
            # '0',                         WAT         17
            # '0',                         LED_1 (CC)    18
            # '0',                         LED_2 (Alt) 19
            # '0',                         SIG_LVL        20
            # '',                         RSV            21
            # '3\r'] 0 - 22                BK_DIMMER    22

            screendata = {
                'line1' : displayarray[4].strip(),
                'line2' : displayarray[6].strip(),
                'line3' : displayarray[10].strip(),
                'mode' : displayarray[12].split(),
                'frequency' : displayarray[8].strip(), # text float value
                'squelchmode' : bool(displayarray[14]), # 0 or 1
                'mutemode' : bool(displayarray[15]), # 0 or 1
                'weatheralertstatus' : displayarray[17], # 0 or 1 or $$$
                'ccled' : bool(int(displayarray[18])), # 0 or 1
                'alertled' : bool(int(displayarray[19])), # 0 or 1
                'backlightlevel' : int(displayarray[22].strip()) # 1 - 3
            }

        elif displayarray[1] == '1111':
            # Menu 0 - 18
            # ['STS',
            # '1111',                 DISP_FORM    1
            # ' -- M E N U --  ',     L1_CHAR        2
            # '________________',     L1_MODE        3
            # 'Program System  ',     L2_CHAR     4
            # '****************',     L2_MODE     5
            # 'Program Location',     L3_CHAR     6
            # '',                     L3_MODE     7
            # 'Srch/CloCall Opt',     L4_CHAR     8
            # '',                     L4_MODE     9
            # '1',                     SQL         10
            # '1',                     MUT         11
            # '0',                     RSV         12
            # '0',                     WAT         13
            # '0',                     LED_1         14
            # '0',                   LED_2         15
            # '0',                     SIG_LVL     16
            # '',                     RSV         17
            # '3\r']                BK_DIMMER    18

            screendata = {
                'line1' : displayarray[2].strip(),
                'line2' : displayarray[4].strip(),
                'line3' : displayarray[6].strip(),
                'line4' : displayarray[8].strip(),
                'squelchmode' : bool(displayarray[10]), # 0 or 1
                'mutemode' : bool(displayarray[11]), # 0 or 1
                'weatheralertstatus' : displayarray[13], # 0 or 1 or $$$
                'ccled' : bool(displayarray[14]), # Close Call 0 or 1
                'alertled' : bool(displayarray[15]), # 0 or 1
                'backlightlevel' : int(displayarray[18].strip()) # 1 - 3
            }

        return screendata

    def getreception(self):
        """ Collect Signal strength infomration """
        line = self.sendcommand('GLG', 70)
        gtgarray = line.split(',')

        #GLG,48,NFM,0,0,PortlandCity,Portland Police,Police Disp,1,0,NONE,NONE,
        #GLG,,,,,,,,,

        glgdata = {
            'tgid' : gtgarray[1],
            'mod' : gtgarray[2],
            'att' : int(gtgarray[3]),
            'ctcss' : int(gtgarray[4]),
            'name1' : gtgarray[5],
            'name2' : gtgarray[6],
            'name3' : gtgarray[7],
            'sql' : int(gtgarray[8]),
            'mut' : int(gtgarray[9]),
            'systag' : int(gtgarray[10]),
            'chantag' : int(gtgarray[11])
        }

        return glgdata

    def menu(self, item):

        menuoptions = [ 'SVC_MENU', 'WX_MENU', 'CCBAND_MENU', 'SCR_OPT_MENU',
        'GL_LIST_MENU', 'SETTING_MENU']

        if item in menuoptions:
            commandreturn = self.sendcommand('MNU,' + str(item), 6)
            status = self.checkok(commandreturn)
        else:
            status = False

        return status

    def collectsysteminfo(self):

        # SIH
        # SIH,[SYS_INDEX][\r]
        # SIN
        # SIN,[SYS_TYPE],[NAME],[QUICK_KEY],[HLD],[LOUT],[DLY],[RSV],[RSV],[RSV],[RSV], [RSV],[REV_INDEX],[FWD_INDEX],[CHN_GRP_HEAD],[CHN_GRP_TAIL], [SEQ_NO],[START_KEY],[RECORD],[RSV],[RSV],[RSV],[RSV],[NUMBER_TAG], [RSV],[ RSV],[ RSV],[PROTECT],[STATE][\r]
        # SIT
        # SIT,[SYS_INDEX][\r]

        pass

    def getsignalstrength(self):
        """ Collect Signal strength infomration """
        line = self.sendcommand('PWR', 17)
        powerarray = line.split(',')
        powerpercent = (int(powerarray[1])/1023)*100

        if DEBUG:
            print powerarray

        # Return singal power, and 3 screen lines
        return powerpercent

    def volume(self, setvol=''):
        """ Collect or Set Volume """
        if setvol == '':
            volume = self.sendcommand('VOL', 6)
            status = 'SET'
            volume = volume.split(',')[1]
        else:
            volume = self.sendcommand('VOL,' + str(setvol), 6)
            status = self.checkok(volume)
            volume = setvol

        return status, volume

    def mute(self):

        volume = self.sendcommand('VOL,' + str(0), 6)
        status = self.checkok(volume)

        return status, volume

    def squelch(self, setsql=''):
        """ Collect or set Squelch """
        if setsql == '':
            squelch = self.sendcommand('SQL', 6)
            status = 'SET'
            squelch = squelch.split(',')[1]
        else:
            squelch = self.sendcommand('SQL,' + str(setsql), 6)
            status = self.checkok(squelch)
            squelch = setsql

        return status, squelch

    def getradioinfo(self):
        """ Get Radio information """

        # MDL Get Model Info
        model = self.sendcommand('MDL', 10)
        model = model.split(',')

        # VER Get Firmware Version
        version = self.sendcommand('VER', 10)
        version = version.split(',')

        return version, model

    def pushbutton(self, key, mode, function=False):
        """ Simulate a button push """

        validmodes = ['P', 'L', 'H', 'R']
        validkeys = ['P', 'W', 'G', 'M', 'F', 'H', 'S', 'L', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', 'E', 'Q', 'V', '<', '>']

        if function:
            radioout = self.sendcommand('KEY,F,P', 10)
            self.checkok(radioout)


        if key not in validkeys:
            print 'KEY ERROR'

        if mode not in validmodes:
            print 'MODE ERROR'

        radioin = 'KEY,' + key + ',' + mode

        radioout = self.sendcommand(radioin, 10)
        status = self.checkok(radioout)

        return status
