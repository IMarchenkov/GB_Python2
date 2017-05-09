
# Клиент игры "Запоминалка"

import socket
from datetime import datetime

import transaction

HOST, PORT = 'localhost', 9999

print('Клиент запущен')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
c = transaction.Transaction((1, 236231, 1999999),
                            datetime(2017, 5, 6, 15, 00, 00))
sock.sendall(c.send())

recvd = str(sock.recv(1024), 'utf-8')

print(recvd)

sock.close()

# __add__  ->  +