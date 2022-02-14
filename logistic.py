import random
import paho.mqtt.client as mqtt
from multiprocessing import Process

class mqttSubs():
    def init(self):
        def on_message(client, userdata, message):
            print("message received \n", str(message.payload.decode("utf-8")))

        topic = "testtopic/mqtt/"
        BROKER_ADDRESS = "broker.hivemq.com"
        PORT = 1883
        client_name = str(random.randrange(999))

        client = mqtt.Client(client_name)
        client.on_message = on_message
        client.connect(BROKER_ADDRESS, PORT)  # connect to broker
        client.subscribe(topic+"duration")
        client.subscribe(topic + "transaction")
        client.loop_forever()


if __name__ == '__main__':
    mqtt_thread = Process(target=mqttSubs)
    mqtt_thread.start()
    mqtt_thread.join()