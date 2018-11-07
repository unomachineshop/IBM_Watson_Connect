import time
import sys
import uuid
import argparse
import os
import ibmiotf.device
from pathlib import Path

# Command processing function for specified device
def commandProcessor(cmd):
	print("Command received: %s" % cmd.data)

# Initialize the device client
try:
	# Retrieve config file parameters from config file located in same working directory
	options = ibmiotf.device.ParseConfigFile(os.path.join(Path().absolute(), "device.cfg"))
	# Apply config file parameters to client device
	client = ibmiotf.device.Client(options)
	# Define the callback function for client device
	client.commandCallback = commandProcessor
	# Connect the device to IBM Watson
	client.connect()
except ibmiotf.ConnectionException as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Send the datapoint(s) to IBM Watson
for x in range (0, 10):
	# Data payload to be sent to IBM Watson
	data = { 'simpledev' : 'ok', 'x' : x}
	# Publishing event callback function
	def myOnPublishCallback():
		print("Confirmed event %s received by IoTF\n" % x)
	# Now the actual event is published to IBM Watson
	success = client.publishEvent("event", "json", data, qos=0, on_publish=myOnPublishCallback)
	
	if not success:
		print("Not connected to IBM Watson")
		sys.exit()

	time.sleep(1)

# Disconnect the device and application from the cloud
client.disconnect()