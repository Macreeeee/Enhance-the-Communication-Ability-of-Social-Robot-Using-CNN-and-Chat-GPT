from naoqi import ALProxy
import subprocess
import json
import time
import datetime
import keyboard
import os
import socket
from Tkinter import *
from gui import *

nao = False
path_to_nao_audio = 'nao@nao.local:/home/nao/recordings/recording.wav'
path_to_pc_audio = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/recordings/recording.wav'
path_to_nao_picture = 'nao@nao.local:/home/nao/recordings/cameras'
path_to_pc_picture = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/recordings/pictures'
#
# def bind_socket():
#     global s, conn, addr
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind(('localhost', 5000))
#     s.listen(1)
#     conn, addr = s.accept()

# Call chat gpt through recorded json file.
def call_gpt():
    command = "python D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src\chat.py"
    output = subprocess.check_output(command, shell=True)
    return output

# Send audio recording .wav to Vosk model.
def speech_recognition(path):
    command = "python D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/speech_to_text.py " + path
    output = subprocess.check_output(command, shell=True)
    output = output.split('\n')

    return output

# Transfer recording.wav from NAO to src.
def file_transfer(path1, path2):
    command = 'pscp -pw nao {} {}'.format(path1, path2)
    subprocess.call(command, stdout=open(os.devnull, 'wb'))
    # command = "plink -l nao -pw nao nao@nao.local 'rm /home/nao/recordings/recording.wav'"

# def load_fer_model():
#     global conn
#     response = "load_fer_model"
#     conn.sendall(response.encode())
#
# def fer_predict():
#     global conn
#     response = "run_fer_model"
#     conn.sendall(response.encode())



# Initially create or re-write communication recording.json with basic chat-GPT content.
# Initially create or re-write communication recording.txt with time.
def initial_communication_background():
    content = "Your name is NAO, you are a robot. Today is Sunday."
    communication = [{"role": "system", "content": content}]

    json_dict = dict()
    json_dict['log'] = communication
    json_object = json.dumps(json_dict, indent=4)
    # Initialize json file
    with open("./recordings/communication_recording.json", "w+") as outfile:
        outfile.write(json_object)
    # Initialize txt file
    with open("./recordings/communication_recording.txt", "a") as outfile:
        outfile.write('===================================\n')
        outfile.write('Recording Date: {}\n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

# Add new communication dialog to communication recording json.
def add_new_content(role, content):
    log = json.load(open("./recordings/communication_recording.json", "r"))
    log['log'].append({"role": role, "content": content})
    json_object = json.dumps(log, indent=4)

    with open("./recordings/communication_recording.json", "w+") as outfile:
        outfile.write(json_object)
    with open("./recordings/communication_recording.txt", "a") as outfile:
        outfile.write('\n{}  {}: {}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), role, content))

def take_picture_dataset():
    emotion_folder_list = ['anger', 'disgust', 'sad', 'surprise', 'neutral']
    for e in emotion_folder_list:
        try:
            os.mkdir(path_to_pc_picture + '/' + e)
        except:
            pass
        textToSpeechProxy.say(e)
        time.sleep(0.5)
        for i in range(10):
            textToSpeechProxy.say(str(i))
            time.sleep(0.5)
            photoCaptureProxy.takePictures(1, "/home/nao/recordings/cameras/", "image")
            file_transfer(path_to_nao_picture + '/image.jpg', path_to_pc_picture + '/{}/image{}.jpg'.format(e, str(i)))
    textToSpeechProxy.say('picture taking done. thanks for participating!')
    exit()

if __name__ == "__main__":
    root = Tk()
    root.title("Communication Manager")
    app = Application(master=root)
    app.mainloop()
    root.destroy()

    print('GUI finished. Exit')
    exit()


    path_to_nao_audio = 'nao@nao.local:/home/nao/recordings/recording.wav'
    path_to_pc_audio = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/recordings/recording.wav'
    path_to_nao_picture = 'nao@nao.local:/home/nao/recordings/cameras'
    path_to_pc_picture = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/recordings/pictures'

    initial_communication_background()
    if nao:
        IP = "nao.local"
        PORT = 9559
        # motion = ALProxy("ALMotion", IP, PORT)
        textToSpeechProxy = ALProxy("ALTextToSpeech", IP, PORT)
        audioRecorderProxy = ALProxy("ALAudioRecorder", IP, PORT)
        # asr = ALProxy("ALSpeechRecognition", IP, PORT)
        # asr.setVocabulary(['over'], False)
        # asr.subscribe("WordRecognized")
        # asr.signal.connect(on_word_recognized)

        # moodProxy = ALProxy("ALMood", IP, PORT)
        # print moodProxy.currentPersonState()
        # print moodProxy.getEmotionalReaction()
        photoCaptureProxy = ALProxy("ALPhotoCapture", IP, PORT)
        photoCaptureProxy.setResolution(0)
        photoCaptureProxy.setPictureFormat("jpg")
        photoCaptureProxy.setColorSpace(0)

        # take_picture_dataset()
        # audioRecorderProxy.stopMicrophonesRecording()

        # Main loop goes here
        while True:
            audioRecorderProxy.startMicrophonesRecording("/home/nao/recordings/recording.wav",  'wav', 16000, (0,0,1,0))
            print "Audio record started."
            last_time = time.time()
            while True:
                current_time = time.time()
                if current_time - last_time >= 1:
                    last_time = current_time
                    nao_picture_path_list = photoCaptureProxy.takePictures(1, "/home/nao/recordings/cameras/", "image")
                    file_transfer(path_to_nao_picture + '/image.jpg', path_to_pc_picture + '/tmp_image.jpg')
                    # predict  = fer_predict()
                    # print(predict)
                    # print 'picture took {}'.format(current_time)
                if keyboard.is_pressed("p"):
                    print 'keyboard interrupt'
                    break
                if keyboard.is_pressed("q"):
                    print 'end conversation'
                    audioRecorderProxy.stopMicrophonesRecording()
                    exit()
            audioRecorderProxy.stopMicrophonesRecording()
            print 'recording over'

            file_transfer(path_to_nao_audio, path_to_pc_audio)
            output = speech_recognition(path_to_pc_audio)
            print(output[0])
            print(output[2])
            print('user: ' + output[1])
            add_new_content('user', output[1])

            response = call_gpt()
            print('NAO: ' + response)
            add_new_content('assistant', response)

            textToSpeechProxy.say(response)
    else:
        while True:
            output = speech_recognition('')
            try:
                print(output[0])
                print(output[2])
                print('user: ' + output[1])
                add_new_content('user', output[1])

                response = call_gpt()
                print('NAO: ' + response)
                add_new_content('assistant', response)
            except:
                exit()



