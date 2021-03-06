# This script receives and processes the data that the NODEMCU module (that has the IR BEAM break sensor attached to it) sends via MQTT protocol
import paho.mqtt.client as mqtt
from twilio.rest import Client
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(24,GPIO.IN)
GPIO.setup(21,GPIO.IN)


 
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    #Mqtt topic
    client.subscribe("esp/test")
    client.subscribe("esp/test")
 

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
  
    if GPIO.input(21) and GPIO.input(24):
    # this condition is used to halt the sysytem when both the face recognition and the fingerprint module give a positive answer for recognition of the user
        print("Hello user, the system is halted for 30 seconds")
        time.sleep(30)

    if msg.payload == "1":
        print("Motion detected, intruder alert")
        
        from twilio.rest import Client
        # Twilio web service packages and libraries to make the call to the user
        account_sid = "AC0ae86014fe91789e86a3e4195125709f"
        auth_token = "0b3c35d9918e9d4fa12d1d454f7e60ba"
        client = Client(account_sid, auth_token)
        print "calling....."
        
        call = client.calls.create(
        to="The number to be called",
        from_="Your Twilio number",
        url="http://demo.twilio.com/docs/voice.xml"
        )
        i=1
        while i<6:
             
            GPIO.output(17,GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(17,GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(17,GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(17,GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(17,GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(17,GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(17,GPIO.LOW)
            time.sleep(0.2)
            i=i+1
        time.sleep(10)


    if msg.payload == "0":
        print("No motion detected")
        
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect("IP of the Raspberry pi on which the MQTT server is running", 1883, 60)
 
client.loop_forever()
