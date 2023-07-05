from vosk import Model, KaldiRecognizer
import sys
import json
import os
import pyaudio
import argparse
import time

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


# parser = argparse.ArgumentParser()
# parser.add_argument('--p', args=None, default=None)
# args = parser.parse_args()
# if args.p:
stream = open(sys.argv[1], "rb")
# else:
#     # Used for microphone realtime input:
#     mic = pyaudio.PyAudio()
#     stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
#     stream.start_stream()

start = time.time()
total = []
while True:
    data = stream.read(4096)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        res = json.loads(rec.Result())
        # print(res)
        # if res['text'][-4:] == 'over':
        #     res['text'] = res['text'][:-4]
        #     break
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
