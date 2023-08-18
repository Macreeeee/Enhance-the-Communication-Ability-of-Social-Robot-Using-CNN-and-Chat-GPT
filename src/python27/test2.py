from main import file_transfer
import time

path_to_nao_audio = 'nao@nao.local:/home/nao/recordings/recording.wav'
path_to_pc_audio = './recordings/recording.wav'
path_to_nao_picture = 'nao@nao.local:/home/nao/recordings/cameras'
path_to_pc_picture = './recordings/pictures'

n = 1
# file_transfer(path_to_nao_picture + '/image.jpg', path_to_pc_picture + '/tmp_image.jpg')
# file_transfer(path_to_nao_audio, path_to_pc_audio)


# start = time.time()
# for i in range(n):
#     file_transfer(path_to_nao_picture + '/image.jpg', path_to_pc_picture + '/tmp_image.jpg')
# end = time.time()
# print((end-start)/n)


start = time.time()
for i in range(n):
    file_transfer(path_to_nao_audio, path_to_pc_audio)
end = time.time()
print((end-start)/n)
# import matplotlib.pyplot as plt
# import PIL
# import time
#
#
# ml = ['anger', 'disgust','happy', 'neutral', 'sad', 'surprise']
# plt.title('Self-created data set')
# for i in range(len(ml)):
#     path = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/recordings\pictures/{}/image{}.jpg'
#     img = PIL.Image.open(path.format(ml[i], '3'))
#     plt.subplot(2, 6, i + 1)
#     plt.title(ml[i])
#     plt.axis('off')
#     plt.imshow(img)
#
#     img = PIL.Image.open(path.format(ml[i], '13'))
#     plt.subplot(2, 6, i + 7)
#     # plt.title(ml[i])
#     plt.axis('off')
#     plt.imshow(img)
#
# plt.show()


# import matplotlib.pyplot as plt
#
# plt.bar(['Deepface', 'FER', 'FCNN+HCC'], [72, 73, 68])
# plt.xlabel('Model Name')
# plt.ylabel('Accuracy (%)')
# plt.title('Accuracy Comparison using self-created data set')
# plt.show()

# import socket
# from test import *
# from Tkinter import *
# import matplotlib.pyplot as plt
#
# def t1():
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind(('localhost', 5000))
#     s.listen(1)
#     conn, addr = s.accept()
#     data = conn.recv(1024)
#     print(data.decode())
#     response = "Hello from Python 3.x!"
#     conn.sendall(response.encode())
#     conn.close()
#     s.close()
#
#
# def print_var():
#     print(var)
#
# class Application(Frame):
#     def __init__(self, master=None):
#         Frame.__init__(self, master)
#         self.DO = Button(self)
#         self.DO2 = Button(self)
#         self.log_window = Text(self)
#         self.pack()
#         self.createWidgets()
#
#     def add_log(self, log, empty_line=True, color="black"):
#         if empty_line:
#             self.log_window.insert(END, '\n' + log, color)
#         else:
#             self.log_window.insert(END, log, color)
#         self.log_window.update()
#
#     def createWidgets(self):
#         self.DO["text"] = "do"
#         self.DO["fg"] = "red"
#         self.DO["command"] = sleep_do
#         self.DO.grid(row=1, column=0)
#
#         self.DO2["text"] = "do2"
#         self.DO2["fg"] = "red"
#         self.DO2["command"] = sleep_do
#         self.DO2.grid(row=2, column=0)
#
#         self.log_window.grid(row=0, column=1)
#
# if __name__ == '__main__':
#     t1()
