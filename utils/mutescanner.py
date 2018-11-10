#!/usr/bin/which python3
# Mute Uniden BCT15X Scanner 
#
# Author: Ben Mason
# Version: 0.1
#
import pyuniden

__author__ = "Ben Mason"
__version__ = "0.1"
__email__ = "locutus@the-collective.net"
__status__ = "Development"

PORT = '/dev/ttyACM0'
SPEED = 115200

scanner = pyuniden.Unidenrc()
scanner.openserial(PORT, SPEED)
scanner.mute()
scanner.closeserial()

