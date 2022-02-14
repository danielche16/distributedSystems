import sys
sys.path.append(r'C:\\PyghonProgramms\\gen-py')

from tutorial import Example
from tutorial.ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from multiprocessing import Process
import os
import requests
import socket
import datetime
import time

class ExampleHandler:
    def send(self, WAREHOUSE: int, action: str, name: str, product_id: str, value: str):
        port = str(8000 + WAREHOUSE)
        os.environ['NO_PROXY'] = '127.0.0.1'
        requests.get('http://127.0.0.1:' + port + "/receive-" + product_id + "-" + value)
        ts = time.time()
        print("\n<The Thrift server handled you request successfully> " + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
        return

    def content(self, WAREHOUSE: int):
        port = 8000 + WAREHOUSE
        ip = '127.0.0.1'
        answer = "-"
        thriftServer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        thriftServer_socket.connect((ip, port))
        thriftServer_socket.sendall("GET /print HTTP/1.1".encode())

        answer: str = thriftServer_socket.recv(1024).decode()
        thriftServer_socket.close()
        print(answer)
        return answer

    def send_sendGoods(self, WAREHOUSE, action, name, productId, value, targetoff):
        port = str(8000 + WAREHOUSE)
        os.environ['NO_PROXY'] = '127.0.0.1'
        requests.get('http://127.0.0.1' + port + "/receive" + productId + "-" + value)
        ts = time.time()
        print("\n<The Thrift server handled you request successfully> " + datetime.datetime.fromtimestamp(ts).strftime(
            '%Y-%m-%d %H:%M:%S'))
        return


class thriftServer:
    def __init__(self):
        handler = ExampleHandler()

        processor = Example.Processor(handler)
        transport = TSocket.TServerSocket("0.0.0.0", 9090)
        transportFactory = TTransport.TBufferedTransportFactory()
        protocolFactory = TBinaryProtocol.TBinaryProtocolFactory()

        server = TServer.TThreadedServer(processor, transport, transportFactory, protocolFactory)
        print("\n Thrift Server is being started")
        server.serve()


if __name__ == '__main__':
    x = Process(target=thriftServer)
    x.start()
    x.join()
