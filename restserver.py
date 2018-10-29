#!/usr/bin/which python3
# Mute Uniden BCT15X Scanner
#
# Author: Ben Mason
# Version: 0.1
#
import web
import unidenbct15x

__author__ = "Ben Mason"
__copyright__ = "Copyright 2017"
__version__ = "0.1"
__email__ = "locutus@the-collective.net"
__status__ = "Development"

PORT = '/dev/ttyACM0'
SPEED = 115200

URLS = (
    '/mute', 'mute',
    '/volume/(.*)', 'volume'
)

class mute:
    def GET(self):
    	scanner = unidenbct15x.Unidenbct15x()
        scanner.openserial(PORT, SPEED)
        status, volume = scanner.mute()
        scanner.closeserial()

        return status, volume

class volume:
    def GET(self, setvol=''):
        scanner = unidenbct15x.Unidenbct15x()
        scanner.openserial(PORT, SPEED)
        status, volume = scanner.volume(setvol)
        scanner.closeserial()

        return status, volume

if __name__ == "__main__":

    app = web.application(URLS, globals())

    app.run()
