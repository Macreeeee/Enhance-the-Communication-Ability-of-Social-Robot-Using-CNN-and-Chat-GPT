from naoqi import ALProxy
import subprocess
import json
import time
import datetime
import keyboard
import os

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
        outfile.write('Recording Date: {}\n'.format(datetime.datetime.now()))

# Add new communication dialog to communication recording json.
def add_new_content(role, content):
    log = json.load(open("./communication_recording.json", "r"))
    log['log'].append({"role": role, "content": content})
    json_object = json.dumps(log, indent=4)

    with open("./recordings/communication_recording.json", "w+") as outfile:
        outfile.write(json_object)
    with open("./recordings/communication_recording.txt", "a") as outfile:
        outfile.write('{}  {}: {}'.format(datetime.datetime.now(), role, content))

def on_word_recognized(value):
    print("Recognized word:", value)


if __name__ == "__main__":

    path_to_nao_audio = 'nao@nao.local:/home/nao/recordings/recording.wav'
    path_to_pc_audio = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/recordings/recording.wav'
    path_to_nao_picture = 'nao@nao.local:/home/nao/recordings/cameras'
    path_to_pc_picture = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/recordings/pictures'

    initial_communication_background()

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
    photoCaptureProxy.setResolution(2)
    photoCaptureProxy.setPictureFormat("jpg")

    # nao_picture_path_list = photoCaptureProxy.takePictures(1, "/home/nao/recordings/cameras/", "image")
    # file_transfer(path_to_nao_picture, path_to_pc_picture)
    # exit()
    # audioRecorderProxy.stopMicrophonesRecording()
    # exit()
    while True:
        audioRecorderProxy.startMicrophonesRecording("/home/nao/recordings/recording.wav",  'wav', 16000, (0,0,1,0))
        print "Audio record started."
        last_time = time.time()
        while True:
            current_time = time.time()
            if current_time - last_time >= 1:
                last_time = current_time
                nao_picture_path_list = photoCaptureProxy.takePictures(1, "/home/nao/recordings/cameras/", "image")
                file_transfer(path_to_nao_picture + '/image.jpg', path_to_pc_picture + '/image{}.jpg'.format(current_time))
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
        exit()
        textToSpeechProxy.say(response)



