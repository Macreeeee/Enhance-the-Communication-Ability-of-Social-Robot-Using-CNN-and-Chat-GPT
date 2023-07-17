from Tkinter import *
import socket
from main import *
import time
import subprocess


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.CLEAR_LOG = Button(self)
        self.QUIT = Button(self)
        self.INITIAL = Button(self)
        self.log_window = Text(self)
        self.recording_window = Text(self)
        # self.picture_window = Label(self, image=)
        self.pack()

        self.createWidgets()

    def load_fer_model(self):
        self.add_log('Loading face expression recognition model: self trained CNN ...')
        response = "load_fer_model"
        self.conn_fer.sendall(response.encode())
        while True:
            response = self.conn_fer.recv(1024)
            if response.decode() == 'fer_model_loaded':
                self.add_log('face expression recognition model loaded')
                break
            if response.decode() == 'fer_model_load_failed':
                self.add_log('face expression recognition model failed to load')
                break

    def load_stt_model(self):
        self.add_log('Loading speech to text model: VOSK')
        response = "load_stt_model"
        self.conn_stt.sendall(response.encode())
        while True:
            response = self.conn_stt.recv(1024)
            if response.decode() == 'stt_model_loaded':
                self.add_log('speech to text model loaded')
                break
            if response.decode() == 'stt_model_load_failed':
                self.add_log('speech to text model failed to load')
                break

    def read_recording(self):
        for line in self.recording_file.readlines():
            self.recording_window.insert(END, line)
            # self.content.see(END)

    def add_recording(self, txt):
        self.recording_window.insert(END, txt)

    def add_log(self, log):
        self.log_window.insert(END, '\n' + log)
        self.log_window.update()

    def clear_recording(self):
        self.recording_window.delete('1.0', END)
        self.add_log('Communication recording cleared')

    def on_quit(self):
        self.add_log('Quit application, please wait...')
        response = "quit"
        self.conn_fer.sendall(response.encode())
        self.conn_stt.sendall(response.encode())
        time.sleep(1)
        self.s.close()
        self.quit()

    def initial_build(self):
        self.add_log('initial building...')

        self.recording_file = open(
            'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/recordings\communication_recording.txt',
            'r')
        self.read_recording()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('localhost', 5000))
        self.s.listen(2)

        subprocess.Popen("python face_expression_recognition.py")
        self.conn_fer, self.addr_fer = self.s.accept()
        time.sleep(1)
        subprocess.Popen("python speech_to_text.py")
        self.conn_stt, self.addr_stt = self.s.accept()
        print('connect all accepted')

        self.load_fer_model()

        self.load_stt_model()

    def createWidgets(self):
        self.recording_window.grid(row=0, column=0)

        self.log_window.grid(row=0, column=1)

        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.on_quit
        self.QUIT.grid(row=1, column=0)

        self.CLEAR_LOG["text"] = "clear recording",
        self.CLEAR_LOG["command"] = self.clear_recording
        self.CLEAR_LOG.grid(row=1, column=1)

        self.INITIAL["text"] = "initial build",
        self.INITIAL["command"] = self.initial_build
        self.INITIAL.grid(row=1, column=2)


if __name__ == '__main__':
    root = Tk()
    root.title("Communication Manager")
    app = Application(master=root)
    app.mainloop()
    root.destroy()
