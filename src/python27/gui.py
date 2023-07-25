from Tkinter import *
import socket
from main import *
import time
import subprocess
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

        self.CLEAR_LOG = Button(self)
        self.QUIT = Button(self)
        self.INITIAL = Button(self)
        self.START = Button(self)
        self.TEST = Button(self)

        self.ENABLE_FR = Button(self)
        self.ENABLE_ACTION = Button(self)

        self.log_window = Text(self)
        self.recording_window = Text(self)

        sample_img=ImageTk.PhotoImage(Image.open("recordings/pictures/User_Icon.jpg"))
        self.picture_window = Label(self, image=sample_img, width=160, height=120)
        self.picture_window.img = sample_img

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

    def start_communication(self):
        nao = False
        # path_to_nao_audio = 'nao@nao.local:/home/nao/recordings/recording.wav'
        # path_to_pc_audio = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/recordings/recording.wav'
        # path_to_nao_picture = 'nao@nao.local:/home/nao/recordings/cameras'
        # path_to_pc_picture = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/recordings/pictures'

        self.add_log('\ncommunication started', color='blue')
        initial_communication_background()
        self.recording_window.delete('1.0', END)
        self.read_recording()
        self.log_window.update()

        if nao:
            IP = "nao.local"
            PORT = 9559
            textToSpeechProxy = ALProxy("ALTextToSpeech", IP, PORT)
            audioRecorderProxy = ALProxy("ALAudioRecorder", IP, PORT)

            photoCaptureProxy = ALProxy("ALPhotoCapture", IP, PORT)
            photoCaptureProxy.setResolution(0)
            photoCaptureProxy.setPictureFormat("jpg")
            photoCaptureProxy.setColorSpace(0)

            # Main loop goes here
            while True:
                audioRecorderProxy.startMicrophonesRecording("/home/nao/recordings/recording.wav", 'wav', 16000,
                                                             (0, 0, 1, 0))
                print
                "Audio record started."
                last_time = time.time()
                while True:
                    current_time = time.time()
                    if current_time - last_time >= 1:
                        last_time = current_time
                        nao_picture_path_list = photoCaptureProxy.takePictures(1, "/home/nao/recordings/cameras/",
                                                                               "image")
                        file_transfer(path_to_nao_picture + '/image.jpg', path_to_pc_picture + '/tmp_image.jpg')
                        self.conn_fer.sendall('run_fer_model'.encode())
                        prediction = wait_until_receive(self.conn_fer)
                        print(prediction)
                        # print 'picture took {}'.format(current_time)
                    if keyboard.is_pressed("p"):
                        print
                        'keyboard interrupt'
                        break
                    if keyboard.is_pressed("q"):
                        print
                        'end conversation'
                        audioRecorderProxy.stopMicrophonesRecording()
                        exit()
                audioRecorderProxy.stopMicrophonesRecording()
                print
                'recording over'

                file_transfer(path_to_nao_audio, path_to_pc_audio)
                self.conn_stt.sendall('run_stt_model'.encode())
                text = wait_until_receive(self.conn_stt)
                add_new_content('user', text)

                response = call_gpt()
                print('NAO: ' + response)
                add_new_content('assistant', response)

                textToSpeechProxy.say(response)
        else:
            end = False
            while not end:
                self.conn_stt.sendall('run_stt_model'.encode())
                msg = wait_until_receive(self.conn_stt)
                add_new_content('user', msg.decode())
                response = call_gpt()
                print('NAO: ' + response)
                add_new_content('assistant', response)

                self.read_recording()
                self.log_window.update()
                for eos in ['goodbye', 'Goodbye', 'bye', 'Bye']:
                    if eos in response:
                        end = True
            self.add_log('communication ended', color='blue')

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

    def initial_build(self):
        self.add_log('initial building...', color='blue')

        self.recording_file = open(
            'recordings/communication_recording.txt',
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
        self.picture_window.grid(row=0, column=2)
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
        self.QUIT.grid(row=1, column=0)

        self.CLEAR_LOG["text"] = "clear recording",
        self.CLEAR_LOG["command"] = self.clear_recording
        self.CLEAR_LOG.grid(row=1, column=1)

        self.INITIAL["text"] = "initial build",
        self.INITIAL["command"] = self.initial_build
        self.INITIAL.grid(row=1, column=2)

        self.START["text"] = "start communication",
        self.START["command"] = self.start_communication
        self.START.grid(row=1, column=3)

        self.TEST["text"] = "test",
        self.TEST["command"] = self.refresh_picture
        self.TEST.grid(row=1, column=4)


if __name__ == '__main__':
    root = Tk()
    root.title("Communication Manager")
    app = Application(master=root)
    app.mainloop()
    root.destroy()
