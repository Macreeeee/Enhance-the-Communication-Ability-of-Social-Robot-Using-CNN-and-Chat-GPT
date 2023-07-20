import socket
from test import *


def t1():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 5000))
    s.listen(1)
    conn, addr = s.accept()
    data = conn.recv(1024)
    print(data.decode())
    response = "Hello from Python 3.x!"
    conn.sendall(response.encode())
    conn.close()
    s.close()


def print_var():
    print(var)


if __name__ == '__main__':
    t1()
