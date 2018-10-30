#!/usr/bin/which python3
# Group 2 enable/disable Uniden BCT15X Scanner 
#
# Author: Ben Mason
# Version: 0.1
#
import unidenbct15x

__author__ = "Ben Mason"
__copyright__ = "Copyright 2017"
__version__ = "0.1"
__email__ = "locutus@the-collective.net"
__status__ = "Development"

PORT = '/dev/ttyACM0'
SPEED = 115200

scanner = unidenbct15x.Unidenbct15x()
scanner.openserial(PORT, SPEED)
scanner.pushbutton("2","P",function=True)
scanner.closeserial()

