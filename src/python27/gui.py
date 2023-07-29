from Tkinter import *
import socket
from main import *
import time
import subprocess
import threading
from PIL import ImageTk, Image


def wait_until_receive(conn):
    while True:
        msg = conn.recv(1024)
        if msg:
            response = msg.decode()
            break
    return response


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.recording_file = open(
            'recordings/communication_recording.txt',
            'r')
        self.CLEAR_LOG = Button(self)
        self.QUIT = Button(self)
        self.INITIAL = Button(self)
        self.START = Button(self)
        self.stopping = False
        self.STOP = Button(self, text="stop communication", command=self.on_stop)
        self.TEST = Button(self)

        self.nao = BooleanVar()
        self.NAO = Checkbutton(self, text="nao available", variable=self.nao).grid(row=10, column=0)

        self.ENABLE_FR = Button(self)
        self.ENABLE_ACTION = Button(self)

        self.socket_input_label = Label(self, text="GUI socket port:")
        self.socket_input = Entry(self)
        self.socket_input.insert(0, '5000')

        self.log_window = Text(self)
        self.recording_window = Text(self)

        sample_img = ImageTk.PhotoImage(Image.open("recordings/pictures/User_Icon.jpg"))
        self.picture_window = Label(self, image=sample_img, width=160, height=120)
        self.picture_window.img = sample_img

        self.pack()

        self.createWidgets()

    def start_task(self, time, command):
        self.after(time, command)

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
            self.recording_window.update()
            # self.content.see(END)

    def add_recording(self, txt):
        self.recording_window.insert(END, txt)

    def add_log(self, log, empty_line=True, color="black"):
        if empty_line:
            self.log_window.insert(END, '\n' + log, color)
        else:
            self.log_window.insert(END, log, color)
        self.log_window.update()

    def clear_recording(self):
        self.recording_window.delete('1.0', END)
        self.add_log('Communication recording cleared')

    def refresh_picture(self):
        tmp_img = ImageTk.PhotoImage(Image.open("recordings/pictures/tmp_image.jpg"))
        self.picture_window.configure(image=tmp_img)
        self.picture_window.img = tmp_img
        # self.picture_window.update()

    def audio_thread(self):
        while not self.stopping:
            if self.nao.get():
                IP = nao_IP
                PORT = 9559
                audioRecorderProxy = ALProxy("ALAudioRecorder", IP, PORT)
                audioRecorderProxy.startMicrophonesRecording("/home/nao/recordings/recording.wav", 'wav', 16000,
                                                             (0, 0, 1, 0))
                time.sleep(7)
                audioRecorderProxy.stopMicrophonesRecording()
                self.conn_stt.sendall('run_stt_model'.encode())
                text = wait_until_receive(self.conn_stt)
                add_new_content('user', text)
                self.read_recording()
                response = call_gpt()
                print('NAO: ' + response)
                add_new_content('assistant', response)
                textToSpeechProxy.say(response)
                self.read_recording()
            else:
                self.conn_stt.sendall('run_stt_model_pc'.encode())
                text = wait_until_receive(self.conn_stt)
                add_new_content('user', text)
                self.read_recording()
                response = call_gpt()
                print('NAO: ' + response)
                add_new_content('assistant', response)
                self.read_recording()
        self.add_log('Communication ended', color='blue')
        self.stopping = False
        self.stop['state'] = NORMAL

    def video_thread(self):
        pass

    def start_communication_version1(self):
        self.add_log('NAO enable: {}'.format(self.nao.get()), color='blue')
        threading.Thread(target=self.audio_thread).start()

    def on_stop(self):
        self.add_log('\nTrying to end communication, please wait...', color='grey')
        if not self.stopping:
            self.stopping = True
            self.STOP['state'] = DISABLED

    def on_quit(self):
        self.add_log('\nQuit application, please wait...', color='blue')
        try:
            response = "quit"
            self.conn_fer.sendall(response.encode())
            self.conn_stt.sendall(response.encode())
            time.sleep(1)
            self.s.close()
            self.quit()
        except:
            self.quit()

    def run_initial_build(self):
        threading.Thread(target=self.initial_build).start()

    def initial_build(self):
        subprocesses = ['stt', 'fer']

        self.add_log('initial building with functions: {}...'.format(subprocesses), color='blue')
        # self.add_log('NAO enable: {}'.format(self.nao.get()), color='blue')
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind(('localhost', int(self.socket_input.get())))
            self.add_log('Socket connected to port {}'.format(self.socket_input.get()), color='blue')
        except:
            self.add_log(
                'Socket failed to connected to port {}, please try another port'.format(self.socket_input.get()),
                color='blue')
            return
        self.s.listen(len(subprocesses))

        for sp in subprocesses:
            if sp == 'fer':
                subprocess.Popen("python face_expression_recognition.py {}".format(self.socket_input.get()))
                self.conn_fer, self.addr_fer = self.s.accept()
                print('fer connect accepted')
                self.load_fer_model()
                print('fer model loaded')
            if sp == 'stt':
                subprocess.Popen("python speech_to_text.py {}".format(self.socket_input.get()))
                self.conn_stt, self.addr_stt = self.s.accept()
                print('stt connect accepted')
                self.load_stt_model()
                print('stt model loaded')
            else:
                print('Zero subprocess given. Please check name of subprocess and run initial again.')
            # time.sleep(1)
        print('Initial build successfully')

    def createWidgets(self):
        self.recording_window.grid(row=0, column=0)
        self.read_recording()
        self.log_window.grid(row=0, column=2)
        self.picture_window.grid(row=0, column=1)
        self.add_log("Welcome to NAO's communication manager.", color='blue')
        self.add_log("Press 'initial build' for initialization. \nPress 'start "
                     "communication for start communication. \nNote: you must do initial building before start "
                     "communication. ", True, 'grey')
        self.log_window.tag_config("grey", foreground="black")
        self.log_window.tag_config("grey", foreground="grey")
        self.log_window.tag_config("red", foreground="red")
        self.log_window.tag_config("blue", foreground="blue")
        # self.log_window.tag_add("blue", "1.0", "1.0 lineend")
        # self.log_window.tag_add("grey", "2.0", "3.0 lineend")
        # self.log_window.tag_add("red", "4.0", "4.5")
        # self.log_window.tag_add("grey", "2.0", "3.0 lineend")

        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.on_quit
        self.QUIT.grid(row=20, column=0)

        self.CLEAR_LOG["text"] = "clear recording",
        self.CLEAR_LOG["command"] = self.clear_recording
        self.CLEAR_LOG.grid(row=2, column=0)

        self.socket_input_label.grid(row=3, column=0)
        self.socket_input.grid(row=3, column=1)

        self.INITIAL["text"] = "initial build",
        self.INITIAL["command"] = self.run_initial_build
        self.INITIAL.grid(row=4, column=0)

        self.START["text"] = "start communication",
        self.START["command"] = self.start_communication_version1
        self.START.grid(row=5, column=0)

        self.STOP["text"] = "stop communication",
        self.STOP["command"] = self.on_stop
        self.STOP.grid(row=7, column=0)

        self.TEST["text"] = "test",
        self.TEST["command"] = self.refresh_picture
        self.TEST.grid(row=6, column=0)


if __name__ == '__main__':
    root = Tk()
    root.title("Communication Manager")
    app = Application(master=root)
    app.mainloop()
    root.destroy()
