from naoqi import ALProxy
import subprocess
import json
import time


def call_gpt():
    command = "python D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src\chat_test.py"
    # command += content

    # Run the command in the terminal
    output = subprocess.check_output(command, shell=True)
    print(output)
    return output


def speech_recognition(path):
    command = "python D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/vosk_test.py " + path
    output = subprocess.check_output(command, shell=True)
    output = output.split('\n')
    print(output[0])
    print(output[2])
    print('you said: ' + output[1])
    return output[1]

def file_transfer():
    command = 'pscp -pw nao nao@nao.local:/home/nao/recordings/recording.wav D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/recordings/recording.wav'
    op = subprocess.check_output(command)
    print 'transfer file from nao to pc'
    # command = "plink -l nao -pw nao nao@nao.local 'rm /home/nao/recordings/recording.wav'"
    # op = subprocess.check_output(command)
    # print 'delete original audio file in nao'

# TODO: save communication recording
def initial_communication_background():
    content = "Your name is NAO, you are a robot. Today is Sunday."

    communication = [{"role": "system", "content": content}]

    json_dict = dict()
    json_dict['log'] = communication

    # Serializing json
    json_object = json.dumps(json_dict, indent=4)

    # Writing to sample.json
    with open("./communication_recording.json", "w+") as outfile:
        outfile.write(json_object)

def add_new_content(role, content):

    log = json.load(open("./communication_recording.json", "r"))
    log['log'].append({"role": role, "content": content})
    json_object = json.dumps(log, indent=4)

    # Writing to sample.json
    with open("./communication_recording.json", "w+") as outfile:
        outfile.write(json_object)
    # print log
    # return log
    # with open('./communication_recording.json', 'w+') as openfile:
    #     # Reading from json file
    #     communication = dict(openfile.readline())
    #     print(openfile.readline())
    #     communication['log'].append({"role": role, "content": content})
    #     json_object = json.dumps(communication)
    #     openfile.write(str(communication))


if __name__ == "__main__":
    initial_communication_background()

    IP = "nao.local"
    PORT = 9559
    # motion = ALProxy("ALMotion", IP, PORT)
    tts = ALProxy("ALTextToSpeech", IP, PORT)
    audioRecorderProxy = ALProxy("ALAudioRecorder", IP, PORT)
    asr = ALProxy("ALSpeechRecognition", IP, PORT)
    # motion.moveInit()
    # motion.moveTo(0.5, 0, 0) # (x; y; theta)

    # arp = ALProxy("ALAudioRecorderProxy", IP, PORT)
    # channels = ALValue
    for i in range(2):
        conversion_dict = {'time':time.time()}
        # videoRecorderProxy.setFrameRate(10.0)
        # videoRecorderProxy.setResolution(2)  # Set resolution to VGA (640 x 480)
        # We'll save a 5 second video record in /home/nao/recordings/cameras/
        audioRecorderProxy.startMicrophonesRecording("/home/nao/recordings/recording.wav",  'wav', 16000, (0,0,1,0))
        print "Audio record started."

        time.sleep(5)
        audioRecorderProxy.stopMicrophonesRecording()
        print 'record over'

        file_transfer()
        txt = speech_recognition('D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/recordings/recording.wav')
        add_new_content('user', txt)

        response = call_gpt()
        add_new_content('assistant', response)

        tts.say(response)


