#!/usr/bin/which python3
# Mute Uniden BCT15X Scanner 
#
# Author: Ben Mason
# Version: 0.1
#
import sys
import unidenbct15x

__author__ = "Ben Mason"
__copyright__ = "Copyright 2017"
__version__ = "0.1"
__email__ = "locutus@the-collective.net"
__status__ = "Development"

PORT = '/dev/ttyUSB0'
SPEED = 115200

setvol = sys.argv[1]

scanner = unidenbct15x.Unidenbct15x()
scanner.openserial(PORT, SPEED)
print ('Setting Volume to {0}'.format(setvol))
scanner.volume(setvol)
scanner.closeserial()

