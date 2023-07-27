import socket
from test import *
from Tkinter import *


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

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.DO = Button(self)
        self.DO2 = Button(self)
        self.log_window = Text(self)
        self.pack()
        self.createWidgets()

    def add_log(self, log, empty_line=True, color="black"):
        if empty_line:
            self.log_window.insert(END, '\n' + log, color)
        else:
            self.log_window.insert(END, log, color)
        self.log_window.update()

    def createWidgets(self):
        self.DO["text"] = "do"
        self.DO["fg"] = "red"
        self.DO["command"] = sleep_do
        self.DO.grid(row=1, column=0)

        self.DO2["text"] = "do2"
        self.DO2["fg"] = "red"
        self.DO2["command"] = sleep_do
        self.DO2.grid(row=2, column=0)

        self.log_window.grid(row=0, column=1)

if __name__ == '__main__':
    t1()
