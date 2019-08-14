import explorerhat
import paho.mqtt.client as mqtt
import time

leftMotor = explorerhat.motor.one
rightMotor = explorerhat.motor.two
roverMotorMqttTopic = "/rover/motor"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: %s" % rc)
    client.subscribe(roverMotorMqttTopic)


def on_disconnect(client, userdata, rc):
    print("Disconnected with result code: %s" % rc)


def on_message(client, userdata, msg):
    print("{0} - {1} ".format(msg.topic, str(msg.payload)))
    motor(msg.payload)


def stop():
    leftMotor.stop()
    rightMotor.stop()


def forward():
    leftMotor.forward()
    rightMotor.forward()


def backwards():
    leftMotor.backwards()
    rightMotor.backwards()


def left():
    leftMotor.forward()
    rightMotor.stop()


def right():
    leftMotor.stop()
    rightMotor.forward()


def circle_left():
    leftMotor.backwards()
    rightMotor.forward()


def circle_right():
    leftMotor.forward()
    rightMotor.backwards()


def motor(direction):
    switcher = {
        b'0': stop,
        b'1': forward,
        b'2': left,
        b'3': right,
        b'6': backwards,
        b'7': circle_left,
        b'8': circle_right
    }

    func = (switcher.get(direction))
    if func is not None:
        func()


client = mqtt.Client('rpirover', mqtt.MQTTv311)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message


client.connect("localhost")

client.loop_start()


while True: ## sleep forever
    time.sleep(999999)
