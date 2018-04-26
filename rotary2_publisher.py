



#!/usr/bin/python
import pika
 
# Use plain credentials for authentication
mq_creds  = pika.PlainCredentials(
    'controlPublisher', 'LightMyPhone')
 
# Use localhost
mq_params = pika.ConnectionParameters(
    host         = "localhost",
    credentials  = mq_creds,
    virtual_host = "/",
    heartbeat_interval=0)
 
# Anyone subscribing to topic "mymessages" receives our messages
mq_exchange    = "amq.topic"
mq_routing_key = "test"
 
# This a connection object
mq_conn = pika.BlockingConnection(mq_params)
 
# This is one channel inside the connection
mq_chan = mq_conn.channel()
 
import readline



import sys
import time
from rotary_class import RotaryEncoder
# Define GPIO inputs
PIN_A = 4 # Pin 8
PIN_B = 25  # Pin 10
BUTTON = 21 # Pin 7

global SkipMessage
SkipMessage = 0


print("Press Ctrl+C to quit.\n")
 
while True:
#  text = raw_input("Enter your message: ")
#  print("Sending '" + text + "'")
#  mq_chan.basic_publish(
#      exchange    = mq_exchange,
#      routing_key = mq_routing_key,
#      body        = text)

	# This is the event callback routine to handle events
	def switch_event(event):
	 global SkipMessage
	 if event == RotaryEncoder.CLOCKWISE:
	 	if SkipMessage == 0:	 		
		   text=";INPUT;RE2CW"
		   mq_chan.basic_publish(
			 exchange    = mq_exchange,
			 routing_key = mq_routing_key,
			 body        = text)
		   print text
		   SkipMessage = SkipMessage + 1
		elif SkipMessage < 3:
		   SkipMessage = SkipMessage + 1
		else:
		   SkipMessage = 0
			
	 elif event == RotaryEncoder.ANTICLOCKWISE:
	 	if SkipMessage == 0:	
		   text=";INPUT;RE2CCW"
		   mq_chan.basic_publish(
			 exchange    = mq_exchange,
			 routing_key = mq_routing_key,
			 body        = text)
		   print text
		   SkipMessage = SkipMessage + 1
		elif SkipMessage < 3:
		   SkipMessage = SkipMessage + 1
		else:
		   SkipMessage = 0
	 print SkipMessage	   
	 return 
	 
	# Define the switch
	rswitch = RotaryEncoder(PIN_A,PIN_B,BUTTON,switch_event)
	while True:
	 time.sleep(2.0)
	 SkipMessage = 0
	 print 'reset'
	 