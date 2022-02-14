import socket
import time
import sys
import random

console_input = sys.argv[2]
offset = console_input[-1]
with open("C:\\PyghonProgramms\\warehouse_data\\warehouse_" + offset + ".data",
          'r') as fr:
    lines = fr.read().split('\n')
    product_list = [x.split('|') for x in lines]


class udp_sensor:
    udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, ip: str, port: int) -> None:
        self.UDP_IP_ADDRESS = ip
        self.UDP_PORT_NO = port
        self.SENSOR_ID = str(sys.argv[1])

    def udp_send(self, data: str) -> bool:
        udp_sensor.udp_client_socket.connect((self.UDP_IP_ADDRESS, self.UDP_PORT_NO))
        udp_sensor.udp_client_socket.send(data.encode())
        with open('./sensor_logfiles/sensor_log_' + self.SENSOR_ID + '.data', 'a') as file_reader:
            file_reader.write(data + '|' + self.UDP_IP_ADDRESS + ":" + str(self.UDP_PORT_NO) + "\n")
        print(udp_sensor.udp_client_socket.recv(1024).decode())


sensor = udp_sensor("127.0.0.1", int(sys.argv[2]))
ACTIONS = ["in", "out", " inv "]

while True:
    random_number = random.randrange(6)
    random_action = random.randrange(2)
    sensor.udp_send(ACTIONS[random_action] + '|' + product_list[random_number][0] + '|' + product_list[random_number][
        1] + '|' + str(random.randrange(50)))
    time.sleep(0.1)
