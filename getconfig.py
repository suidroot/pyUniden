#!/usr/bin/which python3
# Mute Uniden BCT15X Scanner 
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

SPEED = 115200
#PORT = '/tmp/ttyV0'
PORT = '/dev/ttyUSB0'

scanner = unidenbct15x.Unidenbct15x()
scanner.openserial(PORT, SPEED)
scanner.getconfiguration()
scanner.closeserial()

