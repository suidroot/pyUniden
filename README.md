# pyUniden
Python Library for the Uniden Scanners using the Serial interface protocol. 

This library has been tested on the Uniden BCT15X and BCD996P2. These both use a simlar command set. 

```
PORT = '/dev/ttyACM0'
SPEED = 115200

scanner = pyuniden.Unidenrc()
scanner.openserial(PORT, SPEED)
scanner.pushbutton("2","P",function=True)
scanner.closeserial()
```

## Uniden Protocol Specs
http://info.uniden.com/twiki/pub/UnidenMan4/BCT15XFirmwareUpdate/BCT15X_v1.03.00_Protocol.pdf
http://info.uniden.com/twiki/pub/UnidenMan4/BCD996P2/BCD996P2_Remote_Protocol_ver_1_03.pdf

