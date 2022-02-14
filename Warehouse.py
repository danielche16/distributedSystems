import socket
from datetime import datetime
from multiprocessing import Process
import csv
import sys
import json
import subprocess
import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
import requests
import random

from tutorial import Example
from tutorial.ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

# defining the path variable outside any scope, so its easier to change
#!TODO Change the path to -> "yourProjectpath"\\warehouse_data\\warehouse_
warehouse_data_path = "C:\\PyghonProgramms\\warehouse_data\\warehouse_"

class thriftClient:
    def startup(to_do: str, WAREHOUSE: int, action: str, name: str, product_id: str, value: str, target: int):
        # Init thrift connection and protocol handlers
        transport = TSocket.TSocket("127.0.0.1", 9090)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)

        # Set client to our WarehouseManager
        client = Example.Client(protocol)

        # Connect to server
        transport.open()

        if 'send' in to_do:
            client.send(WAREHOUSE, action, name, product_id, value)
        elif 'content' in to_do:
            # print(str(client.content(WAREHOUSE)))
            return client.content(WAREHOUSE)
        if 'sendGoods' in to_do:
            client.sendGoods(WAREHOUSE, action, name, product_id, value, target)



        transport.close()


class warehouse_management:

    def load_data(warehouse_id: int) -> list:
        try:
            file = open(
                warehouse_data_path + str(
                    warehouse_id) + ".data", "r+")
        except:
            file = open(
                warehouse_data_path + str(
                    warehouse_id) + ".data", "x")
            return list()
        csv_reader = csv.reader(file, delimiter="|")
        data = list(csv_reader)
        return data

    def change_data(warehouse_id: int, action: str, name: str, id: str, quantity: int, targ="0") -> int:
        # loading the data from the sender -> opening his inventory
        value = quantity
        warehouse_data = warehouse_management.load_data(warehouse_id)
        file = open(
            warehouse_data_path + str(
                warehouse_id) + ".data", "w")
        for element in warehouse_data:
            if id in element:
                if action == "out":
                    if int(element[2]) - quantity < 0:
                        print("\n Error: You cant send that much goods. You have " + str(element[2])
                              + " and you are trying to send " + str(quantity))
                        value = warehouse_management.search_mqtt(id, warehouse_id, quantity-int(element[2]), targ)
                        element[2] = str(int(element[2]) - int(element[2]))
                    else:
                        thriftClient.startup("send", int(targ), "in", "unknown", id, str(value))
                        element[2] = str(int(element[2]) - value)
                else:
                    element[2] = str(int(element[2]) + quantity)

                for data in warehouse_data:
                    file.write("|".join(data) + "\n")
                return value

        if action == 'in':
            warehouse_data.append([name, id, str(quantity)])
            for data in warehouse_data:
                if data != []:
                    file.write("|".join(data) + "\n")
            return value

    def search_mqtt(id: str, warehouse_id: int, quantity: int, target: str) -> int:
        currQuantity = quantity
        for x in range(1, 9):
            if x == warehouse_id or x == int(target):
                continue
            else:
                try:
                    file = open("C:\\PyghonProgramms\\mqtt_files\\warehouse_" + str(x) + ".data", "r")
                    csv_reader = csv.reader(file, delimiter="|")
                    data = list(csv_reader)
                    for element in data:
                        if id in element:
                            diff = int(element[2]) - quantity
                            if diff > 0:
                                if currQuantity > diff:
                                    requests.get(
                                        'http://127.0.0.1:' + str(8000 + x) + "/send-" + id + "-" + str(diff) + "-" + str(
                                            warehouse_id))
                                    #thriftClient.startup("send", warehouse_id, "in", "unknown", id, str(diff))
                                    #thriftClient.startup("send", int(target), "in", "unknown", id, str(diff))
                                    currQuantity -= diff
                                else:
                                    requests.get('http://127.0.0.1:' + str(8000 + x) + "/send-" + id + "-" + str(
                                        currQuantity) + "-" + target)
                                    #thriftClient.startup("send", warehouse_id, "in", "unknown", id, str(currQuantity))
                                    #thriftClient.startup("send", int(target), "in", "unknown", id, str(currQuantity))
                                    return quantity
                except:
                    break

        return quantity - currQuantity

def subscribeTopic(topic:str) -> None:
    print("Implement the subscription here")

def publishInventory(WAREHOUSE_ID: str) -> None:
    # mqtt client
    TOPIC = "testtopic/mqtt/inventory" + WAREHOUSE_ID
    BROKER_ADDRESS = "broker.hivemq.com"
    PORT = 1883
    client_name = str(random.randrange(999))
    client = mqtt.Client(client_name)
    client.connect(BROKER_ADDRESS, PORT)

    data_dir = warehouse_data_path + WAREHOUSE_ID
    with open(data_dir + ".data") as file_in:
        lines = []
        lines.append(WAREHOUSE_ID)
        for line in file_in:
            lines.append(line)

    log_data = lines
    joined_log_data = "\n".join(log_data)

    client.publish(TOPIC, joined_log_data, qos=1)
    client.loop()
    return None

def publish_sensor(WAREHOUSE_ID: str, data: str) -> None:
    # mqtt client, broker address and topic to subscribe/unsubscribe
    topic = "testtopic/mqtt/sensor"
    broker = "broker.hivemq.com"
    PORT = 1883
    client_name = str(random.randrange(999))
    client = mqtt.Client(client_name)
    client.connect(broker, PORT)
    WAREHOUSE_MESSAGE = "Warehouse: " + WAREHOUSE_ID + " | "
    client.publish(topic, WAREHOUSE_MESSAGE + " " + data, qos=1)
    client.loop()
    return None

class mqttSubs():
    def __init__(self):
        def on_message(client, userdata, message):
            with open("./mqtt_files/warehouse_" + str(message.payload.decode("utf-8"))[0] + ".data", 'w') as f:
                f.write(str(message.payload.decode("utf-8")))



        topic = "testtopic/mqtt/"
        broker = "broker.hivemq.com"
        PORT = 1883
        client_name = str(random.randrange(999))

        client = mqtt.Client(client_name)
        client.on_message = on_message
        client.connect(broker, PORT)  # connect to broker
        client.subscribe(topic)
        client.loop_forever()


class warehouse_http_server:
    def __init__(self, WAREHOUSE: str):
        WAREHOUSE_ID = WAREHOUSE
        SERVER_HOST = '0.0.0.0'
        SERVER_PORT = 8000 + int(WAREHOUSE)

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(2)

        while True:
            # waiting for client
            client_connection, client_address = server_socket.accept()
            client_connection.setblocking(False)

            # receive client request
            request = None
            while request == None:
                try:
                    request = client_connection.recv(1024).decode()
                    print(request)
                except:
                    pass

            referer = False
            try:
                url = request.splitlines()
            except:
                pass
            try:
                url = (url[0].split(' '))[1]
            except:
                pass
            # sending a http response to client
            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            if 'warehouse_log' in url:
                data_dir = "C:\\PyghonProgramms\\warehouse_logfiles\\warehouse_" + WAREHOUSE_ID
            elif 'sensor' in url:
                data_dir = "sensor_logfiles/sensor_log_" + url + ".data"
            elif 'send' in url:
                data_dir = warehouse_data_path + WAREHOUSE_ID
                splitted_url = url.split('-')
                product_id = splitted_url[1]
                value = splitted_url[2]
                target_offset = splitted_url[3]
                warehouse_management.change_data(int(WAREHOUSE), "out", "unknown", product_id, int(value), target_offset)
                publishInventory(WAREHOUSE_ID)

                warehouse_data = warehouse_management.load_data(int(WAREHOUSE))
                for element in warehouse_data:
                    if product_id in element:
                        name = element[0]

                with open("./warehouse_logfiles/warehouse_" + str(WAREHOUSE_ID) + ".data", 'a') as f:
                    f.write(" out " + "|" + str(name) + "|" + product_id + "|" + "127.0.0.1:" + str(20000 + int(WAREHOUSE)))
            elif 'receive' in url:
                data_dir = warehouse_data_path + WAREHOUSE_ID
                name = ""
                split_url = url.split('-')
                product_id = split_url[1]
                value = split_url[2]
                warehouse_data = warehouse_management.load_data(int(WAREHOUSE))
                for element in warehouse_data:
                    if product_id in element:
                        name = element[0]
                warehouse_management.change_data(int(WAREHOUSE), "in", name, product_id, int(value))
                publishInventory(WAREHOUSE_ID)

                with open("./warehouse_logfiles/warehouse_" + str(WAREHOUSE_ID) + ".data", 'a') as f:
                    f.write("in" + "|" + name + "|" + product_id + "|" + value + "|" + "127.0.0.1:" + str(
                        20000 + int(WAREHOUSE)) + "\n")

                print("\neverything worked fine")
            elif 'content' in url:
                split_url = url.split('-')
                target_offset = split_url[1]
                if target_offset != WAREHOUSE_ID:
                    answer = str(thriftClient.startup("content", int(target_offset), "", "", "", "", ""))
                    print("\n", answer)
                    client_connection.sendall(answer.encode())
            elif 'print' in url:
                print("\n Lets print")
                data_dir = warehouse_data_path + WAREHOUSE_ID
            elif 'subscribe' in url:
                #!TODO: implement specific subscriptions
                split_url = url.split('-')
                topic = split_url[1]
            elif 'unsubscribe' in url:
                split_url = url.split('-')
                topic = split_url[1]
            elif 'order' in url:
                print("\n Ordering something from another warehouse")
                split_url = url.split('-')
                product_id = split_url[1]
                amount = split_url[2]
                warehouse_target = split_url[3]
                data_dir = warehouse_data_path + WAREHOUSE_ID
                # Do only, when the receiver is not the sender
                if warehouse_target != WAREHOUSE_ID:
                    warehouse_management.change_data(int(warehouse_target), "out", "", product_id, int(amount), WAREHOUSE_ID)
                    publishInventory(WAREHOUSE_ID)

                    warehouse_data = warehouse_management.load_data(int(WAREHOUSE))
                    for element in warehouse_data:
                        if product_id in element:
                            name = element[0]

                        with open("./warehouse_logfiles/warehouse_" + str(warehouse_target) + ".data", 'a') as f:
                            f.write(" out " + "|" + str(name) + "|" + product_id + "|" + "127.0.0.1:" + str(
                                20000 + int(warehouse_target)))


            try:
                print("\ntrying to read the answer")
                with open(data_dir + ".data") as file_in:
                    lines = []
                    for line in file_in:
                        lines.append(line)

                log_data = lines
                joined_log_data = "\n".join(log_data)
                print("read successfully")
            except:
                joined_log_data = "\n<h1>Trying to reach the file went wrong. Contact the System Administrator<h1>"

            response = '\n' + joined_log_data
            header = 'HTTP/1.0 200 OK\n' \
                     'Server: custom python\n' \
                     'Date: ' + date_time + '\n' \
                     'Content-Type: text\n' \
 \

            message = header + response
            client_connection.sendall(message.encode())
            print("\nhave sent")
            client_connection.close()

    def send_http(dataDir: str) -> str:
        with open(dataDir + ".data") as file_in:
            lines = []
            for line in file_in:
                lines.append(line)

        log_data = lines
        joined_log_data = "\n".join(log_data)
        print("\nlesen hat geklappt")
        response = '\n' + joined_log_data
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        header = 'HTTP/1.0 200 OK\n' \
                 'Server: custom python\n' \
                 'Date: ' + date_time + '\n' \
                                        'Content-Type: text\n' \
 \

        message = header + response
        return message



class sensor_udp_server:

    def __init__(self, WAREHOUSE_ID: int):
        UDP_IP_ADDRESS = "127.0.0.1"
        UDP_PORT_NO = 20000 + WAREHOUSE_ID

        serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
        while True:
            data_list = warehouse_management.load_data(WAREHOUSE_ID)
            data, addr = serverSock.recvfrom(1024)
            data = data.decode()
            split_data = data.split("|")
            pubData = " Sensor Type: " + split_data[0] + " | " + "Article ID: "+split_data[2] + " | " +  "Amount: "+split_data[3]
            publish_sensor(str(WAREHOUSE_ID), pubData)
            value = warehouse_management.change_data(WAREHOUSE_ID, split_data[0], split_data[1], split_data[2],
                                             int(split_data[3]))

            publishInventory(str(WAREHOUSE_ID))
            with open("./warehouse_logfiles/warehouse_" + str(WAREHOUSE_ID) + ".data", 'a') as f:
                f.write(data + "|" + addr[0] + ":" + str(UDP_PORT_NO) + "\n")
            serverSock.sendto(str(value).encode(), (addr))

            print("Message: ", data + ";" + addr[0] + ":" + str(UDP_PORT_NO) + "\n")


if __name__ == '__main__':
    sensor_udp_server_thread2 = Process(target=sensor_udp_server, args=(int(sys.argv[1]),))
    sensor_udp_server_thread2.start()

    warehouse_http_server_thread = Process(target=warehouse_http_server, args=(sys.argv[1],))
    warehouse_http_server_thread.start()

    mqttSubs_thread = Process(target=mqttSubs)
    mqttSubs_thread.start()

    sensor_udp_server_thread2.join()
    warehouse_http_server_thread.join()
    mqttSubs_thread.join()
