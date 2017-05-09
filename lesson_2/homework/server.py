
# Сервер игры "Запоминалка"

import socketserver
import random
from datetime import datetime

import transaction

class MemTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.recived = transaction.decode(self.request.recv(1024))
        self.data = transaction.Transaction(self.recived[0], self.recived[1])
        print(self.data)

        print("Клиент {} сообщает {}".format(self.client_address[0], self.data))

          
HOST, PORT = '0.0.0.0', 9999

server = socketserver.TCPServer((HOST, PORT), MemTCPHandler)  
print('Сервер запущен')

server.serve_forever()

