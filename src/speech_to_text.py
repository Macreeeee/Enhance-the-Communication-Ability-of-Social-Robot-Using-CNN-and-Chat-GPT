from vosk import Model, KaldiRecognizer
import sys
import json
import os
import pyaudio
import argparse
import time
from pydub import AudioSegment
import socket
import wave
import numpy as np

path_to_nao_audio = 'nao@nao.local:/home/nao/recordings/recording.wav'
path_to_pc_audio = 'recordings/recording.wav'

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
def read_stt_stream(recorded=True):
    if recorded:
        stream = AudioSegment.from_wav(path_to_pc_audio)
        stream = stream + 20
        stream.export(path_to_pc_audio, "wav")
        stream = open(path_to_pc_audio, "rb")
        # stream = AudioSegment.from_wav(sys.argv[1])
        # stream = stream + 20
        # stream.export(sys.argv[1], "wav")
        # stream = open(sys.argv[1], "rb")
    else:
        # Used for microphone input:
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        stream.start_stream()
        frames = []
        start_time = time.time()
        time_limit = 7
        print('audio record start, time limit: {} seconds'.format(time_limit))
        while time.time() - start_time < time_limit:
            data = stream.read(8192)
            frames.append(data)
        print('audio record end')
        recorded_audio = b''.join(frames)
        stream.stop_stream()
        with wave.open(path_to_pc_audio, 'wb') as wf:
            wf.setnchannels(1)  # Mono channel (change to 2 for stereo)
            wf.setsampwidth(2)  # 2 bytes per sample (change to 1 for 8-bit audio)
            wf.setframerate(16000)  # 16000 samples per second (change to desired rate)
            wf.writeframes(recorded_audio)
        # stream = open(path_to_pc_audio, "rb")
        stream = AudioSegment.from_wav(path_to_pc_audio)
        stream = stream + 20
        stream.export(path_to_pc_audio, "wav")
        stream = open(path_to_pc_audio, "rb")
    return stream


def run_stt_model(stream, rec):
    start = time.time()
    total = []
    while True:
        data = stream.read(8192)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            # print(res)
            # if res['text'][-4:] == 'over':
            #     res['text'] = res['text'][:-4]
            #     total.append(res['text'])
            #     break
            # if res['text'][-4:] == 'quit':
            #     exit()
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
        stream = read_stt_stream(False)
        run_stt_model(stream, rec)
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', int(sys.argv[1])))
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
                    print('error when process stt model, please load model again.')
                    exit(1)
            if response.decode() == 'run_stt_model_pc':
                try:
                    stream = read_stt_stream(False)
                    text = run_stt_model(stream, rec)
                    s.sendall(text.encode())
                except:
                    print('error when process stt model, please load model again.')
                    exit(1)
