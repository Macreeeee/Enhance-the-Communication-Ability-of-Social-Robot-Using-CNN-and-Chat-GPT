import socket
from test2 import *


class Var:
    def __init__(self, var):
        self.var = var


def t1():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 5000))
    data = "Hello from Python 2.7!"
    s.sendall(data.encode())
    response = s.recv(1024)
    print(response.decode())
    s.close()


def define_and_print_var():
    instance = Var(var=1)

    print_var()


if __name__ == '__main__':
    define_and_print_var()
