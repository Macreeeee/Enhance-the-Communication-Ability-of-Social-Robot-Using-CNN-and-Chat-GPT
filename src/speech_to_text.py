from vosk import Model, KaldiRecognizer
import sys
import json
import os
import pyaudio
import argparse
import time
from pydub import AudioSegment
import socket


def load_stt_model():
    path = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/vosk-model-small-en-us-0.15'
    # path = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/vosk-model-en-us-0.22-lgraph'
    if not os.path.exists(path):
        print("no vosk model find")
        exit(1)

    start = time.time()
    model = Model(path)
    rec = KaldiRecognizer(model, 16000)
    end = time.time()
    print('Vosk model loaded, time used: {}'.format(end - start))
    return rec


# parser = argparse.ArgumentParser()
# parser.add_argument('--p', args=None, default=None)
# args = parser.parse_args()
# if args.p:
# stream = open(sys.argv[1], "rb")
def read_stt_stream():
    if len(sys.argv) > 1:
        stream = AudioSegment.from_wav(sys.argv[1])
        stream = stream + 20
        stream.export(sys.argv[1], "wav")
        stream = open(sys.argv[1], "rb")
    else:
        # Used for microphone realtime input:
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        stream.start_stream()
    return stream


def run_stt_model(stream, rec):
    start = time.time()
    total = []
    while True:
        data = stream.read(4096)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            # print(res)
            if res['text'][-4:] == 'over':
                res['text'] = res['text'][:-4]
                total.append(res['text'])
                break
            if res['text'][-4:] == 'quit':
                exit()
            total.append(res['text'])
        # else:
        #     res = json.loads(rec.PartialResult())
        #     # print (res)

    # res = json.loads(rec.FinalResult())
    # print(res)
    # total.append(res['text'])

    print(' '.join(total))
    end = time.time()
    print('speech recognized, time used: {}'.format(end - start))
    return ' '.join(total)


if __name__ == '__main__':
    socket_enable = True
    if not socket_enable:
        rec = load_stt_model()
        stream = read_stt_stream()
        run_stt_model(stream, rec)
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', 5000))
        while True:
            response = s.recv(1024)
            print(response.decode())
            if response.decode() == 'quit':
                s.close()
                exit()
            if response.decode() == 'load_stt_model':
                try:
                    rec = load_stt_model()
                    s.sendall("stt_model_loaded".encode())
                except:
                    s.sendall("stt_model_load_failed".encode())
            if response.decode() == 'run_stt_model':
                try:
                    stream = read_stt_stream()
                    text = run_stt_model(stream, rec)
                    s.sendall(text.encode())
                except:
                    print('error: no stt model loaded')
                    exit(1)
