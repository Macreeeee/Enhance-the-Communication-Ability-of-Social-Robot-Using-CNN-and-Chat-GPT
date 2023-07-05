from naoqi import ALProxy
import subprocess
import json
import time
import datetime
import keyboard

# Call chat gpt through recorded json file.
def call_gpt():
    command = "python D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src\chat_test.py"
    output = subprocess.check_output(command, shell=True)
    print(output)
    return output

# Send audio recording .wav to Vosk model.
def speech_recognition(path):
    command = "python D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/vosk_test.py " + path
    output = subprocess.check_output(command, shell=True)
    output = output.split('\n')
    print(output[0])
    print(output[2])
    print('you said: ' + output[1])
    return output[1]

# Transfer recording.wav from NAO to src.
def file_transfer():
    command = 'pscp -pw nao nao@nao.local:/home/nao/recordings/recording.wav D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/recordings/recording.wav'
    op = subprocess.check_output(command)
    print 'transfer file from nao to pc'
    # command = "plink -l nao -pw nao nao@nao.local 'rm /home/nao/recordings/recording.wav'"
    # op = subprocess.check_output(command)
    # print 'delete original audio file in nao'

# Initially create or re-write communication recording.json with basic chat-GPT content.
# Initially create or re-write communication recording.txt with time.
def initial_communication_background():
    content = "Your name is NAO, you are a robot. Today is Sunday."
    communication = [{"role": "system", "content": content}]

    json_dict = dict()
    json_dict['log'] = communication
    json_object = json.dumps(json_dict, indent=4)
    # Initialize json file
    with open("./communication_recording.json", "w+") as outfile:
        outfile.write(json_object)
    # Initialize txt file
    with open("./communication_recording.txt", "a") as outfile:
        outfile.write('===================================\n')
        outfile.write('Recording Date: {}\n'.format(datetime.datetime.now()))

# Add new communication dialog to communication recording json.
def add_new_content(role, content):
    log = json.load(open("./communication_recording.json", "r"))
    log['log'].append({"role": role, "content": content})
    json_object = json.dumps(log, indent=4)

    with open("./communication_recording.json", "w+") as outfile:
        outfile.write(json_object)
    with open("./communication_recording.txt", "a") as outfile:
        outfile.write('{}  {}: {}'.format(datetime.datetime.now(), role, content))

def on_word_recognized(value):
    print("Recognized word:", value)


if __name__ == "__main__":
    initial_communication_background()

    IP = "nao.local"
    PORT = 9559
    # motion = ALProxy("ALMotion", IP, PORT)
    tts = ALProxy("ALTextToSpeech", IP, PORT)
    audioRecorderProxy = ALProxy("ALAudioRecorder", IP, PORT)
    # asr = ALProxy("ALSpeechRecognition", IP, PORT)
    # asr.setVocabulary(['over'], False)
    # asr.subscribe("WordRecognized")
    # asr.signal.connect(on_word_recognized)
    moodProxy = ALProxy("ALMood", IP, PORT)
    print moodProxy.currentPersonState()
    print moodProxy.getEmotionalReaction()

    exit()
    while True:
        audioRecorderProxy.startMicrophonesRecording("/home/nao/recordings/recording.wav",  'wav', 16000, (0,0,1,0))
        print "Audio record started."
        while True:
            if keyboard.is_pressed("p"):
                print 'keyboard interrupt'
                break
            if keyboard.is_pressed("q"):
                print 'end conversation'
                audioRecorderProxy.stopMicrophonesRecording()
                exit()
        audioRecorderProxy.stopMicrophonesRecording()
        print 'recording over'

        file_transfer()
        txt = speech_recognition('D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/recordings/recording.wav')
        add_new_content('user', txt)

        response = call_gpt()
        add_new_content('assistant', response)

        # tts.say(response)


