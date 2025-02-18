from Tkinter import *
import socket
from main import *
import time
import subprocess
import threading
from PIL import ImageTk, Image
import shutil


def wait_until_receive(conn):
    while True:
        msg = conn.recv(1024)
        if msg:
            response = msg.decode()
            break
    return response


def test_function():
    nao_ip = 'nao.local'
    nao_port = 9559

    motion_proxy = ALProxy("ALMotion", nao_ip, nao_port)
    posture_proxy = ALProxy("ALRobotPosture", nao_ip, nao_port)

    # posture_proxy.goToPosture("Stand", 1.0)
    #
    # motion_proxy.moveTo(-0.3, 0.0, 0, 3)

    motion_proxy.rest()


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.Border = Frame(self, relief='flat', borderwidth=20)

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
        self.NAO_ENABLE = Checkbutton(self)

        self.ENABLE_FR = Button(self)
        self.ENABLE_ACTION = Button(self)

        self.nao_ip_label = Label(self, text="NAO internet address:")
        self.nao_ip = Entry(self)
        self.nao_ip.insert(0, nao_IP)

        self.nao_port_label = Label(self, text="NAO internet port:")
        self.nao_port = Entry(self)
        self.nao_port.insert(0, '9559')

        self.socket_input_label = Label(self, text="GUI socket port:")
        self.socket_input = Entry(self)
        self.socket_input.insert(0, '5000')

        self.openaikey_input_label = Label(self, text="OpenAI API key:")
        self.openaikey_input = Entry(self)

        self.log_window = Text(self, width=90, height=10)
        self.recording_window = Text(self, width=70, height=15)

        w = 160
        h = 120
        sample_img = ImageTk.PhotoImage(Image.open("recordings/pictures/User_Icon.jpg").resize((w, h), Image.ANTIALIAS))
        self.picture_window = Label(self, image=sample_img, width=w, height=h)
        self.picture_window.img = sample_img

        self.emotion_list = []
        self.emotion_label = Label(self)
        self.user_name_label = Label(self)
        self.pack(fill='both', expand=True, padx=10, pady=10)

        self.audio_thread = threading.Thread(target=self.audio_thread_function,
                                             args=(self.nao_ip.get(), self.nao_port.get()))
        self.video_thread = threading.Thread(target=self.video_thread_function,
                                             args=(self.nao_ip.get(), self.nao_port.get()))
        self.face_recognition_thread = threading.Thread(target=self.face_recognition_thread_function)

        self.createWidgets()

    def createWidgets(self):
        self.recording_window.grid(row=0, column=5, rowspan=5, columnspan=4)
        self.read_recording()
        self.log_window.grid(row=6, column=4, rowspan=4, columnspan=7)
        self.picture_window.grid(row=0, column=3, rowspan=4, columnspan=2)

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

        self.socket_input_label.grid(row=0, column=0)
        self.socket_input.grid(row=0, column=1, columnspan=2)

        self.nao_ip_label.grid(row=1, column=0)
        self.nao_ip.grid(row=1, column=1, columnspan=2)

        self.nao_port_label.grid(row=2, column=0)
        self.nao_port.grid(row=2, column=1, columnspan=2)

        self.openaikey_input_label.grid(row=3, column=0)
        self.openaikey_input.grid(row=3, column=1, columnspan=2)

        self.NAO_ENABLE["text"] = "nao available",
        self.NAO_ENABLE["variable"] = self.nao
        self.NAO_ENABLE.grid(row=4, column=0, columnspan=3)

        self.INITIAL["text"] = "initial_build",
        self.INITIAL["command"] = self.run_initial_build
        self.INITIAL.grid(row=5, column=0, columnspan=3)

        self.START["text"] = "start communication",
        self.START["command"] = self.on_start
        self.START.grid(row=6, column=0, columnspan=3)

        self.STOP["text"] = "stop communication",
        self.STOP["command"] = self.on_stop
        self.STOP["state"] = DISABLED
        self.STOP.grid(row=7, column=0, columnspan=3)

        self.CLEAR_LOG["text"] = "clear recording",
        self.CLEAR_LOG["command"] = self.clear_recording
        self.CLEAR_LOG.grid(row=8, column=0, columnspan=3)

        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.on_quit
        self.QUIT.grid(row=9, column=0, columnspan=3)

        self.emotion_label['text'] = 'no emotion detected'
        self.emotion_label.grid(row=5, column=3, columnspan=2)

        self.user_name_label['text'] = '?'
        self.user_name_label.grid(row=4, column=3, columnspan=2)

        # self.TEST["text"] = "test",
        # self.TEST["command"] = self.nao_motion_thread_function
        # self.TEST.grid(row=12, column=0)

    def start_task(self, time, command):
        self.after(time, command)

    def load_fer_model(self):
        self.add_log('Loading face expression recognition model', color='grey')
        response = "load_fer_model"
        self.conn_fer.sendall(response.encode())
        while True:
            response = self.conn_fer.recv(1024)
            if response.decode() == 'fer_model_loaded':
                self.add_log('face expression recognition model loaded', color='grey')
                break
            if response.decode() == 'fer_model_load_failed':
                self.add_log('face expression recognition model failed to load', color='red')
                break

    def load_stt_model(self):
        self.add_log('Loading speech to text model', color='grey')
        response = "load_stt_model"
        self.conn_stt.sendall(response.encode())
        while True:
            response = self.conn_stt.recv(1024)
            if response.decode() == 'stt_model_loaded':
                self.add_log('speech to text model loaded', color='grey')
                break
            if response.decode() == 'stt_model_load_failed':
                self.add_log('speech to text model failed to load', color='red')
                break

    def open_camera(self):
        self.add_log('Trying to open camera on pc')
        response = "camera_open"
        self.conn_cam.sendall(response.encode())
        while True:
            response = self.conn_stt.recv(1024)
            if response.decode() == 'camera_opened':
                self.add_log('Camera opened')
                break
            if response.decode() == 'camera_open_failed':
                self.add_log('Camera open failed')
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
        self.log_window.see(END)
        self.log_window.update()

    def clear_recording(self):
        self.recording_window.delete('1.0', END)
        self.add_log('Communication recording cleared')

    def refresh_picture(self):
        tmp_img = ImageTk.PhotoImage(Image.open("recordings/pictures/tmp_image.jpg"))
        self.picture_window.configure(image=tmp_img)
        self.picture_window.img = tmp_img
        # self.picture_window.update()

    def audio_thread_function(self, nao_ip, nao_port):
        if self.nao.get():
            try:
                # IP = self.nao_ip.get()
                # PORT = int(self.nao_port.get())
                audioRecorderProxy = ALProxy("ALAudioRecorder", nao_ip, nao_port)
                textToSpeechProxy = ALProxy("ALTextToSpeech", nao_ip, nao_port)
                audioDeviceProxy = ALProxy("ALAudioDevice", nao_ip, nao_port)
            except RuntimeError:
                # print('Cannot connect to tcp://{}:{}'.format(nao_ip, nao_port))
                self.add_log('Audio thread can not connect to tcp://{}:{}'.format(nao_ip, nao_port), color='red')
                return

            textToSpeechProxy.say('Let us start talk! Now, please say something to me')
            while not self.stopping:
                audioDeviceProxy.playSine(500, 40, 0, 0.2)
                time.sleep(0.2)
                audioRecorderProxy.startMicrophonesRecording("/home/nao/recordings/recording.wav", 'wav', 16000,
                                                             (0, 0, 1, 0))
                time.sleep(7)
                audioRecorderProxy.stopMicrophonesRecording()
                audioDeviceProxy.playSine(500, 40, 0, 0.2)
                file_transfer(path_to_nao_audio, path_to_pc_audio)
                self.conn_stt.sendall('run_stt_model'.encode())
                text = wait_until_receive(self.conn_stt)

                average_emotion = max(set(self.emotion_list), key=self.emotion_list.count)
                self.emotion_list = []

                text += " ({})".format(average_emotion)
                add_new_content('user', text, self.user_name_label['text'])
                self.read_recording()
                response = call_gpt(self.openaikey_input.get())
                print('NAO: ' + response)
                add_new_content('assistant', response)
                self.read_recording()
                motion_thread = threading.Thread(target=self.nao_motion_thread_function)
                motion_thread.start()
                textToSpeechProxy.say(response)
                motion_thread.join()
        else:
            while not self.stopping:
                self.conn_stt.sendall('run_stt_model_pc'.encode())
                text = wait_until_receive(self.conn_stt)
                add_new_content('user', text, self.user_name_label['text'])
                self.read_recording()
                response = call_gpt(self.openaikey_input.get())
                print('NAO: ' + response)
                add_new_content('assistant', response)
                self.read_recording()
        self.add_log('Audio thread ended', color='blue')

    def take_and_send_picture(self, photoCaptureProxy, conn_fer):
        print('take and send picture')
        photoCaptureProxy.takePictures(1, "/home/nao/recordings/cameras/", "image")
        file_transfer(path_to_nao_picture + '/image.jpg', path_to_pc_picture + '/tmp_image.jpg')
        conn_fer.sendall('run_fer_model'.encode())
        # prediction = wait_until_receive(conn_fer)
        # self.refresh_picture()
        # self.emotion_label['text'] = prediction
        # self.emotion_label.update()

    def update_emotion_label(self, prediction):
        self.emotion_label['text'] = prediction
        self.emotion_label.update()

    def video_thread_function(self, nao_ip, nao_port):
        if self.nao.get():
            try:
                # IP = self.nao_ip.get()
                # PORT = int(self.nao_port.get())
                photoCaptureProxy = ALProxy("ALPhotoCapture", nao_ip, nao_port)
                photoCaptureProxy.setResolution(1)
                photoCaptureProxy.setPictureFormat("jpg")
                photoCaptureProxy.setColorSpace(13)
            except RuntimeError:
                print('Cannot connect to tcp://{}:{}'.format(nao_ip, nao_port))
                self.add_log('Video thread can not connect to tcp://{}:{}'.format(nao_ip, nao_port), color='red')
                return
            while not self.stopping:
                # for i in range(3):
                #     start = time.time()
                self.take_and_send_picture(photoCaptureProxy, self.conn_fer)
                # threading.Thread(target=self.take_and_send_picture, args=(photoCaptureProxy, self.conn_fer)).start()
                prediction = wait_until_receive(self.conn_fer)
                self.emotion_list.append(prediction)
                self.refresh_picture()
                # time.sleep(0.5)
                # end = time.time()
                # print(end - start)
                print('PREDICTION EMOTION:{}'.format(prediction))
                self.after(0, lambda: self.update_emotion_label(prediction))
                # self.emotion_label['text'] = prediction
                # self.emotion_label.update()
        else:
            while not self.stopping:
                self.conn_stt.sendall('take_picture'.encode())
                response = wait_until_receive(self.conn_cam)
                if response == 'picture_took':
                    self.conn_stt.sendall('run_fer_model'.encode())
                    prediction = wait_until_receive(self.conn_fer)
                    self.refresh_picture()
                    self.emotion_label['text'] = prediction
                    self.emotion_label.update()
        self.add_log('Video thread ended', color='blue')

    def face_recognition_thread_function(self, nao_ip, nao_port):
        if not self.nao.get():
            print('Pass face recognition step')
            self.add_log('Pass face recognition step')
            return
        try:
            # IP = self.nao_ip.get()
            # PORT = int(self.nao_port.get())
            audioRecorderProxy = ALProxy("ALAudioRecorder", nao_ip, nao_port)
            textToSpeechProxy = ALProxy("ALTextToSpeech", nao_ip, nao_port)
            audioDeviceProxy = ALProxy("ALAudioDevice", nao_ip, nao_port)
            photoCaptureProxy = ALProxy("ALPhotoCapture", nao_ip, nao_port)
            photoCaptureProxy.setResolution(0)
            photoCaptureProxy.setPictureFormat("jpg")
            photoCaptureProxy.setColorSpace(13)
            photoCaptureProxy.takePictures(1, "/home/nao/recordings/cameras/", "image")
        except RuntimeError:
            print('Cannot connect to tcp://{}'.format(nao_ip))
            self.add_log('Cannot connect to tcp://{}'.format(nao_ip))
            return

        file_transfer(path_to_nao_picture + '/image.jpg', path_to_pc_picture + '/tmp_image.jpg')
        self.conn_fer.send('face_recognition'.encode())
        response = wait_until_receive(self.conn_fer)
        if response == '?':
            textToSpeechProxy.say('Hi, new person! Can you tell me what is your name?')
            audioDeviceProxy.playSine(500, 40, 0, 0.2)
            time.sleep(0.3)
            audioRecorderProxy.startMicrophonesRecording("/home/nao/recordings/recording.wav", 'wav', 16000,
                                                         (0, 0, 1, 0))
            time.sleep(4)
            audioRecorderProxy.stopMicrophonesRecording()
            audioDeviceProxy.playSine(500, 40, 0, 0.2)
            file_transfer(path_to_nao_audio, path_to_pc_audio)
            self.conn_stt.sendall('run_stt_model'.encode())
            text = wait_until_receive(self.conn_stt)
            if text == '.':
                text = 'No-Name'
            text = text.split(' ')[-1].capitalize()
            add_new_content('assistant', 'Alright! Nice to meet you, {}'.format(text))
            self.read_recording()
            textToSpeechProxy.say('Alright! Nice to meet you, {}'.format(text))
            shutil.move('recordings/pictures/tmp_image.jpg', 'recordings/face_data/{}.jpg'.format(text))
            name = text
        else:
            add_new_content('assistant', 'Hi, {}, meet you again'.format(response))
            self.read_recording()
            textToSpeechProxy.say('Hi, {}, meet you again'.format(response))
            name = response
        print('face recognition finished')
        self.user_name_label['text'] = name
        # self.user_name_label.update()

    def run_motion(self, nao_ip, nao_port, motions):
        print('run motion')
        motion_code = """
import naoqi

motion_proxy = ALProxy("ALMotion", '{}', {})
posture_proxy = ALProxy("ALRobotPosture", '{}', {})
""".format(nao_ip, nao_port, nao_ip, nao_port)

        for m in motions:
            motion_code += m + '\n'

        print(motion_code)
        exec(motion_code)

    def nao_motion_thread_function(self):
        print('motion thread start')
        nao_ip = self.nao_ip.get()
        nao_port = int(self.nao_port.get())
        motions = call_gpt_for_instruction(self.openaikey_input.get())[:-2].split('/')
        print(motions)
        subthread = threading.Thread(target=self.run_motion, args=(nao_ip, nao_port, motions))
        subthread.start()
        subthread.join()

    def on_start(self):
        initial_communication_background()
        print('start communication')
        self.START.config(state=DISABLED)
        self.STOP['state'] = NORMAL

        self.add_log('NAO enable: {}'.format(self.nao.get()), color='blue')
        nao_ip = self.nao_ip.get()
        nao_port = int(self.nao_port.get())
        if self.nao.get():
            self.add_log('Connect to NAO with tcp://{}:{}'.format(nao_ip, nao_port), color='grey')
        else:
            self.add_log('Nao disabled.', color='grey')

        print('start face recognition thread')
        self.face_recognition_thread = threading.Thread(target=self.face_recognition_thread_function, args=(nao_ip, nao_port))
        self.face_recognition_thread.start()
        self.face_recognition_thread.join()

        print('start audio thread')
        self.audio_thread = threading.Thread(target=self.audio_thread_function, args=(nao_ip, nao_port))
        self.audio_thread.start()

        print('start video thread')
        self.video_thread = threading.Thread(target=self.video_thread_function, args=(nao_ip, nao_port))
        self.video_thread.start()

    def on_stop(self):
        self.add_log('\nTrying to end communication, please wait...', color='grey')
        if not self.stopping:
            self.stopping = True
            self.STOP['state'] = DISABLED
            self.audio_thread.join()  # Wait for audio_thread to complete
            self.video_thread.join()
            # while not self.audio_thread.is_alive() and not self.video_thread.is_alive():
            self.stopping = False
            self.STOP['state'] = DISABLED
            self.START['state'] = NORMAL
            self.add_log('Communication stopped. You can restart it or quit this application.', color='blue',
                         empty_line=True)

    def on_quit(self):
        self.add_log('\nQuit application, please wait...', color='blue')
        try:
            response = "quit"
            self.conn_fer.sendall(response.encode())
            self.conn_stt.sendall(response.encode())
            # self.conn_cam.sendall(response.encode())
            time.sleep(1)
            self.s.close()
            self.quit()
        except:
            self.quit()

    def run_initial_build(self):
        threading.Thread(target=self.initial_build).start()

    def initial_build(self):
        subprocesses = ['stt', 'fer']
        if not self.nao.get():
            subprocesses = ['stt', 'fer', 'camera']
        self.add_log('initial building start'.format(subprocesses), color='blue', empty_line=True)
        self.add_log('initial building with functions: {}...'.format(subprocesses), color='grey')
        # self.add_log('NAO enable: {}'.format(self.nao.get()), color='blue')
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind(('localhost', int(self.socket_input.get())))
            self.add_log('Application socket use port: {}'.format(self.socket_input.get()), color='grey')
        except:
            self.add_log(
                'Socket failed to connected to port {}, please try another port'.format(self.socket_input.get()),
                color='red')
            return
        self.s.listen(len(subprocesses))

        for sp in subprocesses:
            if sp == 'fer':
                fer_model_name = 'fer'
                subprocess.Popen(
                    "python face_expression_recognition.py {} {}".format(self.socket_input.get(), fer_model_name))
                self.conn_fer, self.addr_fer = self.s.accept()
                self.add_log('fer connect accepted, will use model: {}'.format(fer_model_name), color='grey')
                self.load_fer_model()
                print('fer model loaded')
            if sp == 'stt':
                stt_model_name = 'VOSK'
                subprocess.Popen("python speech_to_text.py {} {}".format(self.socket_input.get(), stt_model_name))
                self.conn_stt, self.addr_stt = self.s.accept()
                self.add_log('stt connect accepted, will use model: {}'.format(stt_model_name), color='grey')
                self.load_stt_model()
                print('stt model loaded')
            if sp == 'camera':
                subprocess.Popen("python video_threading.py {}".format(self.socket_input.get()))
                self.conn_cam, self.addr_cam = self.s.accept()
                print('camera connect accepted')
                self.open_camera()
                print('camera opened')
            else:
                pass
                # print('Zero subprocess given. Please check name of subprocess and run initial again.')
            # time.sleep(1)
        self.add_log('Initial build successfully', color='blue')
        self.add_log('Please press the button: [Start communication]', color='blue')


if __name__ == '__main__':
    root = Tk()
    root.title("Communication Manager")
    app = Application(master=root)
    app.mainloop()
    root.destroy()
