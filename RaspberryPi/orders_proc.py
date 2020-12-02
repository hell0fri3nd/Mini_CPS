#!/usr/bin/python
import serial
import time
import csv
import datetime
import random

# Costants
HISTORYFILE = 'history.csv'
SERIAL_PORT = '/dev/ttyACM0'

s = serial.Serial(SERIAL_PORT, 9600)
# Arduino reset after enabling serial connection, wait some seconds
print("\n")
print("//////////////////////////////////////////////////")
print("\\\----------------------------------------------\\\\")
print("\\\-------------- [ ORDER SYSTEM ] --------------\\\\")
print("\\\----------------------------------------------\\\\")
print("//////////////////////////////////////////////////")
print("\n")
time.sleep(5)

# Order's queue
queue = [0,1,2,3,4,5]

# These store the current input
chars = []
line = ''

# Serial status
ser_open = True

def save_in_history(file_name, list_of_elem):
	# Open file in append mode
	with open(file_name, 'ab') as write_obj:
		# Create a writer object from csv module
		csv_writer = csv.writer(write_obj)
		# Add contents of list as last row in the csv file
		csv_writer.writerow(list_of_elem)
	print('--[!] History saved')

def retrieve_history(file_name):
	with open(file_name, 'r') as f:
		reader = csv.reader(f)
		for index, row in enumerate(reader):
			if index == 0:
				chosen_row = row
			else:
				r = random.randint(0, index)
				if r == 0:
					chosen_row = row
		return chosen_row

def try_to_open_new_port():
	ret = False
	test = serial.Serial(baudrate=9600, timeout=0, writeTimeout=0)
	test.port = SERIAL_PORT
	try:
		test.open()
		if test.isOpen():
			test.close()
			ret = True
	except serial.serialutil.SerialException:
		pass
	return ret

try:
	while True:
		if len(queue) > 0:
			try:
				for c in s.read():
					chars.append(c)
					if c == '\n':
						length = len(chars)
						line = ''.join(chars[:length-1])
						# Reading if arduino is idle
						if line == 'idle':
							queue.pop()
							print('--[!] Arduino_status: [BUSY]')
							# Tells arduino to start
							s.write('1')
							time.sleep(10)
						# Reading arduino data
						else:
							print('--[OK] Data received ' + line)
							save_in_history(HISTORYFILE, [datetime.datetime.now(), line])
							print('-- Order_status: [FULFILLED]')
							time.sleep(10)
						line = ''
						chars = []
						print('-- Items in queue: [' + str(len(queue)) + ']')
						time.sleep(5)
			except serial.SerialException  as e:
				# Disconnect of USB->UART occured/Arduino failure
				print('--[!] Arduino failed or disconnected')
				s.close()
				ser_open = False

				# Retrieves data from history to fulfill pending orders
				for order in queue:
					queue.pop()
					hist = retrieve_history(HISTORYFILE)
					print('--[OK] Data auto-generated with history:')
					print('-- ' + str(hist[1]))
					time.sleep(10)

				# Tries to reopen serial port
				print('--[!] Trying to reopen Arduino connection ...')
				ser_open = try_to_open_new_port()
				if ser_open:
					print('--[!] Connection restored')
				else:
					print('--[!] Couldn\'t restore connection')
					time.sleep(15)
		elif len(queue)== 0:
			print('--[IDLE] Waiting for new orders ...')
			time.sleep(20)

			if not ser_open:
                                print('--[!] Trying to reopen Arduino connection ...')
				ser_open = try_to_open_new_port()
				if ser_open:
					s.open()
					print('--[!] Connection restored')
					queue = [0,1,2,3,4,5]
				else:
					 print('--[!] Couldn\'t restore connection')
				time.sleep(10)
except KeyboardInterrupt: s.close()
