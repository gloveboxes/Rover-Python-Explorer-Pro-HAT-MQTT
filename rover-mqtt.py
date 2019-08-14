import explorerhat
import paho.mqtt.client as mqtt
import time

motor1 = explorerhat.motor.one
motor2 = explorerhat.motor.two




def on_connect(client, userdata, flags, rc):
    print("Connected with result code: %s" % rc)
    client.subscribe("/rover/motor")

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code: %s" % rc)


def on_message(client, userdata, msg):
    print("{0} - {1} ".format(msg.topic, str(msg.payload)))
    motor(msg.payload)
    # Do this only if you want to send a reply message every time you receive one
    # client.publish("devices/mqtt/messages/events", "REPLY", qos=1)

def stop():
    motor1.stop()
    motor2.stop()

def forward():
    motor1.forward()
    motor2.forward()

def backwards():
    motor1.backwards()
    motor2.backwards()

def left():
    motor1.stop()
    motor2.forward()

def circle_left():
    motor1.backwards()
    motor2.forward()

def right():
    motor1.forward()
    motor2.stop()

def circle_right():
    motor1.forward()
    motor2.backwards()

def motor(direction):
    switcher = {
        b'0': stop,
        b'1': forward,
        b'2': left,
        b'3': right,
        b'6': backwards,
        b'7': circle_left,
        b'8': circle_right,
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    func = (switcher.get(direction))
    if func is not None:
        func()
    # print(switcher.get(direction, "Invalid month"))



client = mqtt.Client('rpirover', mqtt.MQTTv311)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message


client.connect("localhost") # connect to local mosquitto service for testing purposes

client.loop_start()


while True:
    time.sleep(999999)


motor1.forward()
motor2.forward()