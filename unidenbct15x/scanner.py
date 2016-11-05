import serial

DEBUG = False #True

def openserial(port, speed):
	ser = serial.Serial(port, baudrate=speed, timeout=1, xonxoff=False, 
		rtscts=False, dsrdtr=False)
	print(ser.name)         # check which port was really used

	return ser

def sendcommand(ser, command, returnlength):

	ser.write(command + '\r')     # write a string
	ser.flush()
	line = ser.read(returnlength)

	if DEBUG:
		print line

	if 'ERR' in line:
		print "INVALID COMMAND!!!!"

	return line

def checkok(radiooutput):

	radiooutput = radiooutput.split(',')[1]
	radiooutput = radiooutput.strip()

	if radiooutput != 'OK':
		print "ERROR"
		status = False
	else:
		status = True

	return status

def collectscreen(ser):

	line = sendcommand(ser, 'STS', 136)
	displayarray = line.split(',')

	if DEBUG:
		print displayarray

	if displayarray[1] == '011000':
		# Home Screen
		# ['STS', 
		# '011000', 				DISP_FORM	1
		# '                ', 		L1_CHAR		2
		# '', 						L1_MODE		3
		# 'PortlandCity    ', 		L2_CHAR		4
		# '', 						L2_MODE		5
		# 'H   ID SEARC \x81  ', 	L3_CHAR		6
		# '', 						L3_MODE		7
		# ' 852.7875       ', 		L4_CHAR		8
		# '', 						L4_MODE		9
		# 'S0:----------   ', 		L5_CHAR		10
		# '', 						L5_MODE		11
		# '              WX',		L6_CHAR		12 		
		# '', 						L6_MODE		13
		# '1', 						SQL 		14
		# '1', 						MUT 		15
		# '0', 						RSV			16
		# '0', 						WAT 		17
		# '0', 						LED_1 (CC)	18
		# '0', 						LED_2 (Alt) 19
		# '0', 						SIG_LVL		20
		# '', 						RSV			21
		# '3\r'] 0 - 22				BK_DIMMER	22

		line1 = displayarray[4].strip()
		line2 = displayarray[6].strip()
		line3 = displayarray[10].strip()
		modes = displayarray[12].split()

		frequency = displayarray[8].strip() # text float value
		squelchmode = bool(displayarray[14]) # 0 or 1
		mutemode = bool(displayarray[15]) # 0 or 1
		weatheralertstatus = displayarray[17] # 0 or 1 or $$$
		ccled = bool(int(displayarray[18])) # 0 or 1
		alertled = bool(int(displayarray[19])) # 0 or 1

		backlightlevel = int(displayarray[22].strip()) # 1 - 3

		return line1, line2, line3, ccled, alertled, frequency # modes

	elif displayarray[1] == '1111':
		# Menu 0 - 18
		# ['STS', 			
		# '1111', 				DISP_FORM	1
		# ' -- M E N U --  ', 	L1_CHAR		2
		# '________________', 	L1_MODE		3
		# 'Program System  ', 	L2_CHAR 	4
		# '****************', 	L2_MODE 	5
		# 'Program Location', 	L3_CHAR 	6
		# '', 					L3_MODE 	7
		# 'Srch/CloCall Opt', 	L4_CHAR 	8
		# '', 					L4_MODE 	9
		# '1', 					SQL 		10
		# '1', 					MUT 		11
		# '0', 					RSV 		12
		# '0', 					WAT 		13
		# '0', 					LED_1 		14
		# '0',   				LED_2 		15
		# '0', 					SIG_LVL 	16
		# '', 					RSV 		17
		# '3\r']				BK_DIMMER	18

		line1 = displayarray[2].strip()
		line2 = displayarray[4].strip()
		line3 = displayarray[6].strip()
		line4 = displayarray[8].strip()

		squelchmode = bool(displayarray[10]) # 0 or 1
		mutemode = bool(displayarray[11]) # 0 or 1

		weatheralertstatus = displayarray[13] # 0 or 1 or $$$
		ccled = bool(displayarray[14]) # Close Call 0 or 1
		alertled = bool(displayarray[15]) # 0 or 1

		backlightlevel = int(displayarray[18].strip()) # 1 - 3


		return line1, line2, line3, line4, ccled, alertled

def signalstrength(ser):

	line = sendcommand(ser, 'PWR', 17)
	powerarray = line.split(',')
	powerpercent = (int(powerarray[1])/1023)*100

	if DEBUG:
		print powerarray

	# Return singal power, and 3 screen lines
	return powerpercent

def volume(ser, setvol=''):

	if setvol == '':
		volume = sendcommand(ser, 'VOL', 6)
		status = 'SET'
		volume = volume.split(',')[1]
	else:
		volume = sendcommand(ser, 'VOL,' + str(setvol), 6)
		status = checkok(radioout)
		volume = setvol

	return status, volume

def squelch(ser, setsql=''):

	if setsql == '':
		squelch = sendcommand(ser, 'SQL', 6)
		status = 'SET'
		squelch = squelch.split(',')[1]
	else:
		squelch = sendcommand(ser, 'SQL,' + str(setsql), 6)
		status = checkok(radioout)
		squelch = setsql

	return status, squelch

def getinfo(ser):
	
	# MDL Get Model Info
	model = sendcommand(ser, 'MDL', 10)
	model = model.split(',')

	# VER Get Firmware Version	
	version = sendcommand(ser, 'VER', 10)
	version = version.split(',')

	return version, model

def buttonpush(ser, key, mode, function=False):

	validmodes = ['P', 'L', 'H', 'R']
	validkeys = ['P', 'W', 'G', 'M', 'F', 'H', 
	'S', 'L', '1', '2', '3', '4', '5', '6', '7',
	'8', '9', '0', '.', 'E', 'Q', 'V', '<', '>']

	if function == True:
		radioout = sendcommand(ser, 'KEY,F,P', 10)
		checkok(radioout)


	if key not in validkeys:
		print 'KEY ERROR'

	if mode not in validmodes:
		print 'MODE ERROR'

	radioin = 'KEY,' + key + ',' + mode

	radioout = sendcommand(ser, radioin, 10)
	status = checkok(radioout)

	return status

