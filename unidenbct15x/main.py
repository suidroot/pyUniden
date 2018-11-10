#!/usr/bin/which python3
"""
 Library for controlling a Uniden BCT15X scanner
 Author: Ben Mason
 Version: 0.1
"""
# from sys import exit
import serial

DEBUG = False

__author__ = "Ben Mason"
__copyright__ = "Copyright 2017"
__version__ = "0.1"
__email__ = "locutus@the-collective.net"
__status__ = "Development"

def checkok(radiooutput, stricterror=False):
    """ Verify that OK was received back """
    command, radiooutput = radiooutput.split(',')

    if radiooutput == 'NG':
        print "Command: " + command + " no applicable or not available in \
               mode (NG)"
    elif radiooutput == 'ERR':
        print "Command: " + command + " returned and Error"
        status = False
        if stricterror:
            exit("Command: " + command + " returned and Error")
    elif radiooutput != 'OK':
        print "Command: " + command + " did not Return OK"
        status = False
        if stricterror:
            exit("Command: " + command + " did not Return OK")
    else:
        status = True

    return status

class Unidenbct15x(object):
    """ Uniden BCT15X Object """
    ser = None
    numberofsystems = 0
    systems = {}
    groups = {}
    channels = {}

    def ___init___(self):
        """ Init """
        pass

    def openserial(self, port, speed=115200):
        """ Open Serial Port """
        self.ser = serial.Serial(port, baudrate=speed, timeout=1, xonxoff=False,
                                 rtscts=False, dsrdtr=False)

    def closeserial(self):
        """ Close Serial Conenction """
        self.ser.close()

    def sendcommand(self, command, returnlength):
        """ Write to Serial Port and return output """
        self.ser.write(command + '\r')     # write a string
        self.ser.flush()
        # line = self.ser.read(returnlength)
        line = self.ser.readline()
        line = line.rstrip()

        if DEBUG:
            print line

        if 'ERR' in line:
            print "INVALID COMMAND!!!!"

        return line

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
            # 'GRP---------    ',        L6_CHAR        12
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
                'line4' : displayarray[12].split(),
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
        """ WIP """
        menuoptions = ['SVC_MENU', 'WX_MENU', 'CCBAND_MENU',
                       'SCR_OPT_MENU', 'GL_LIST_MENU', 'SETTING_MENU']

        if item in menuoptions:
            commandreturn = self.sendcommand('MNU,' + str(item), 6)
            status = checkok(commandreturn)
        else:
            status = False

        return status

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
            status = checkok(volume)
            volume = setvol

        return status, volume

    def mute(self):
        """ send command to set audio to 0 or mute """
        volume = self.sendcommand('VOL,' + str(0), 6)
        status = checkok(volume)

        return status, volume

    def squelch(self, setsql=''):
        """ Collect or set Squelch """
        if setsql == '':
            squelch = self.sendcommand('SQL', 6)
            status = 'SET'
            squelch = squelch.split(',')[1]
        else:
            squelch = self.sendcommand('SQL,' + str(setsql), 6)
            status = checkok(squelch)
            squelch = setsql

        return status, squelch

    def resumescan(self):
        """ Send button commands to resume Scanning """
        self.pushbutton('S', 'P')

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
        validkeys = ['P', 'W', 'G', 'M', 'F', 'H', 'S', 'L', '1', '2', '3', '4',
                     '5', '6', '7', '8', '9', '0', '.', 'E', 'Q', 'V', '<', '>']

        if function:
            radioout = self.sendcommand('KEY,F,P', 10)
            checkok(radioout)

        if key not in validkeys:
            print 'KEY ERROR'

        if mode not in validmodes:
            print 'MODE ERROR'

        radioin = 'KEY,' + key + ',' + mode

        radioout = self.sendcommand(radioin, 10)
        status = checkok(radioout)

        return status

    def getconfiguration(self):
        """ Gather Information about for all configured
        systems and the assocated groups and channels

        A system in the scanner is made of a root systems which
        links to one or more groups that contain a set of channels.

        Channels are the frequencies

        All data sents itterate using the FWD_INDEX until last sets the next
        item to -1

        OUTPUT: sets the information in object variables
        systems, groups and channels
        """

        # Enter Program mode
        output = self.sendcommand('PRG', 10)
        checkok(output)

        # SCT get quanity of systems
        # output = self.sendcommand('SCT', 10)
        # numberofsystems = int(output.split(',')[1])

        # Get first System
        output = self.sendcommand('SIH', 10)
        print output

        # SIH,1105
        nextsin = output.split(',')[1]
        print nextsin

        # Gather system list, iterate through FWD_INDEX
        # until last system
        while nextsin != -1:
            print "SIN: " + str(nextsin)
            systeminfo = self.getsysteminfo(nextsin)
            self.systems[int(nextsin)] = systeminfo

            nextsin = systeminfo['FWD_INDEX']

        print "----------------------------------"
        for system in self.systems:
            print "SIN: " + str(system)
            print "Group Head: " + str(self.systems[system]['CHN_GRP_HEAD'])

            # Collect Groups for the system
            nextgrp = self.systems[system]['CHN_GRP_HEAD']
            while nextgrp != -1:
                print "GIN: " + str(nextgrp)
                groupout = self.getgroupinformation(nextgrp)
                self.groups[nextgrp] = groupout
                nextchn = self.groups[nextgrp]['CHN_HEAD']

                # Collect Channels for the Group
                while nextchn != -1:
                    print "CIN: " + str(nextchn)
                    channelout = self.getchannelinfo(nextchn)
                    self.channels[nextchn] = channelout
                    nextchn = channelout['FWD_INDEX']

                nextgrp = groupout['FWD_INDEX']

        # exit program mode
        output = self.sendcommand('EPG', 10)
        checkok(output)
        # Set scanner back to scanning mode
        output = self.resumescan()
        # status = checkok(output)

    def getsysteminfo(self, sin):
        """ Gather System information
        INPUT: System ID
        OUTPUT: dict with System details
        """

        output = self.sendcommand('SIN,' + str(sin), 82)
        currentsin = output.split(',')

        if DEBUG:
            print currentsin

        newsin = {
            'SYS_TYPE': currentsin[1],
            'NAME': currentsin[2],
            'QUICK_KEY': currentsin[3],
            'DLY': currentsin[6],
            'REV_INDEX': int(currentsin[12]),
            'FWD_INDEX': int(currentsin[13]),
            'CHN_GRP_HEAD': int(currentsin[14]),
            'CHN_GRP_TAIL': int(currentsin[15]),
            'SEQ_NO': int(currentsin[16]),
            'START_KEY': currentsin[17],
            'RECORD': currentsin[18],
            'PROTECT': bool(int(currentsin[27])),
            'STATE': currentsin[28]
        }

        if currentsin[4] != '':
            newsin['HLD'] = int(currentsin[4])

        if currentsin[5] != '':
            newsin['LOUT'] = bool(int(currentsin[5]))

        if currentsin[23] == 'NONE' or currentsin[23] == '':
            newsin['NUMBER_TAG'] = None
        else:
            newsin['NUMBER_TAG'] = int(currentsin[23])

        return newsin

    def getgroupinformation(self, gin):
        """
        Gather System Group information
        INPUT: Group ID number
        OUTPUT: dict with Group details
        """

        output = self.sendcommand('GIN,' + str(gin), 82)
        currentgin = output.split(',')

        if DEBUG:
            print currentgin

        if currentgin[1] != "ERR\r":

            ginout = {
                'GRP_TYPE' : currentgin[1],
                'NAME' : currentgin[2],
                'LOUT' : bool(int(currentgin[4])),
                'REV_INDEX' : int(currentgin[5]),
                'FWD_INDEX' : int(currentgin[6]),
                'SYS_INDEX' : int(currentgin[7]),
                'CHN_HEAD' : int(currentgin[8]),
                'CHN_TAIL' : int(currentgin[9]),
                'SEQ_NO' : int(currentgin[10]),
                'LATITUDE' : currentgin[11],
                'LONGITUDE' : currentgin[12],
                'RANGE' : int(currentgin[13]),
                'GPS ENABLE' : bool(int(currentgin[14]))
            }

            if currentgin[3] == '.':
                ginout['QUICK_KEY'] = None
            else:
                ginout['QUICK_KEY'] = int(currentgin[3])

            return ginout

        else:
            print "No Group Found"
            return None

    def getchannelinfo(self, cin):
        """
        Gather System Channel Information

        INPUT: Channel ID number
        OUTPUT: Dict containing Channel Detail
        """

        output = self.sendcommand('CIN,' + str(cin), 82)
        currentcin = output.split(',')

        if DEBUG:
            print currentcin

        cinout = {
            'NAME' : currentcin[1],
            'FRQ' : int(currentcin[2]),
            'MOD' : currentcin[3],
            'CTCSS/DCS' : int(currentcin[4]),
            'TLOCK' : bool(int(currentcin[5])),
            'LOUT' : bool(int(currentcin[6])),
            'PRI' : bool(int(currentcin[7])),
            'ATT' : bool(int(currentcin[8])),
            'ALT' : int(currentcin[9]),
            'ALTL' : int(currentcin[10]),
            'REV_INDEX' : int(currentcin[11]),
            'FWD_INDEX' : int(currentcin[12]),
            'SYS_INDEX' : int(currentcin[13]),
            'GRP_INDEX' : int(currentcin[14]),
            'RECORD' : bool(int(currentcin[15])),
            'NUMBER_TAG' : currentcin[18],
            'ALT_PATTERN' : int(currentcin[20]),
            'VOL_OFFSET' : int(currentcin[21])
        }

        return cinout
