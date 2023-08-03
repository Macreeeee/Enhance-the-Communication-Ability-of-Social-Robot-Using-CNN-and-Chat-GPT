from tensorflow import keras
import cv2
import numpy as np
import matplotlib.pyplot as plt
from deepface import DeepFace
from fer import FER
import time
from PIL import Image
import io
import sys
import socket
import os


def face_region(face_cascade, img):
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
    # for (x, y, w, h) in faces:
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    try:
        (x, y, w, h) = faces[0]
        cv2.imwrite('./recordings/pictures/tmp_image.jpg', cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2))
    except:
        print('no face region find, return original image')
        return img
    return img[y:y + h, x:x + w]


def self_trained_cnn(face_cascade, model, image):
    # image = cv2.imread(img_path)
    start = time.time()
    image = face_region(face_cascade, image)

    image = cv2.resize(image, (48, 48))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    predict = model.predict(np.array([image]))
    emotion_list = ['anger', 'disgust', 'happy', 'sad', 'surprise', 'neutral']
    predict = emotion_list[np.argmax(predict)]
    end = time.time()
    print('prediction = {}, time used: {}'.format(predict, end-start))
    return predict


def self_trained_cnn_group_test():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    path = 'fer_model/flicnn_model.keras'
    model = keras.models.load_model(path, compile=False)
    model.compile()
    emotion_list = ['anger', 'disgust', 'happy', 'sad', 'surprise', 'neutral']
    # emotion_list = ['anger', 'neutral', 'sad', 'disgust', 'happy', 'surprise']
    emotion_folder_list = ['anger', 'disgust', 'happy', 'sad', 'surprise', 'neutral']
    map = {'anger': False, 'disgust': False, 'happy': True, 'sad': False, 'surprise': True, 'neutral': True}
    h = 120
    w = 160
    count = 0
    total = 0
    for e in emotion_folder_list:
        for i in range(10):
            total += 1
            image = cv2.imread('./recordings/pictures/{}/image{}.jpg'.format(e, str(i)))
            image = face_region(face_cascade, image)
            # cv2.imwrite('./recordings/pictures/{}/_image{}.jpg'.format(e, str(i)), image)
            start = time.time()
            # image = image[h // 2 - 24:h // 2 + 24, w // 2 - 24:w // 2 + 24]
            image = cv2.resize(image, (48, 48))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            prediction = model.predict(np.array([image]))
            prediction = emotion_list[np.argmax(prediction)]
            end = time.time()
            print('time used: {}'.format(end - start))
            print('true: {}, pre: {}'.format(e, prediction))
            # if map[prediction] == map[e]:
            if prediction == e:
                count += 1
    print(count / total)


def deep_face(img):
    # img = cv2.imread('./recordings/pictures/happy/image1.jpg')
    # plt.imshow(img[:, :, :: -1])
    # start = time.time()
    try:
        result = DeepFace.analyze(img, actions=['emotion'])
        prediction = result[0]['dominant_emotion']
    except:
        prediction = 'None'
    # end = time.time()
    # print(end-start)
    # print(prediction)
    return prediction

    # x1 = int(result[0]['region']['x'])
    # x2 = x1 + int(result[0]['region']['w'])
    # y1 = int(result[0]['region']['y'])
    # y2 = y1 + int(result[0]['region']['h'])
    # plt.imshow(img[y1:y2, x1:x2, :: -1])
    # plt.show()


def deep_face_group_test():
    # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # emotion_list = ['happy']
    emotion_folder_list = ['anger', 'disgust', 'happy', 'sad', 'surprise', 'neutral']
    emotion_list = ['angry', 'disgust', 'happy', 'sad', 'surprise', 'neutral']
    map = {'angry': False, 'disgust': False, 'happy': True, 'sad': False, 'surprise': True, 'neutral': True}
    count = 0
    total = 0
    for e in range(len(emotion_folder_list)):
        for i in range(30):
            total += 1
            img = cv2.imread('./recordings/pictures/{}/image{}.jpg'.format(emotion_folder_list[e], str(i)))
            # img = face_region(face_cascade, img)
            try:
                result = DeepFace.analyze(img, actions=['emotion'])
                prediction = result[0]['dominant_emotion']
            except:
                prediction = 'None'
                total -= 1
            print('true: {}, pre: {}'.format(emotion_folder_list[e], prediction))
            # if map[prediction] == map[e]:
            if prediction == emotion_list[e]:
                count += 1
    print(count / total)


def run_fer(img):
    try:
        result = detector.detect_emotions(img)
        d = result[0]['emotions']
        prediction = max(d, key=d.get)
    except:
        prediction = 'none'
    return prediction


def fer_group_test():
    # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # emotion_list = ['anger']
    emotion_folder_list = ['anger', 'disgust', 'happy', 'sad', 'surprise', 'neutral']
    emotion_list = ['angry', 'disgust', 'happy', 'sad', 'surprise', 'neutral']
    count = 0
    total = 0
    detector = FER()

    for e in range(len(emotion_folder_list)):
        for i in range(30):
            total += 1
            img = cv2.imread('./recordings/pictures/{}/image{}.jpg'.format(emotion_folder_list[e], str(i)))
            # img = face_region(face_cascade, img)

            result = detector.detect_emotions(img)
            try:
                d = result[0]['emotions']
                prediction = max(d, key=d.get)
            except:
                prediction = 'none'
                total -= 1

            print('true: {}, pre: {}'.format(emotion_folder_list[e], prediction))
            if prediction == emotion_list[e]:
                count += 1
    print(count / total)


def face_recognition(img1_path, img2_path):
    try:
        result = DeepFace.verify(img1_path=img1_path, img2_path=img2_path, model_name="VGG-Face",
                                 distance_metric="cosine")
        print(result['distance'])
        result = result['verified']
        print('one face verified')
    except:
        result = False
        print('no face can be recognized')
    return result


def recognition_from_data(img_path, directory):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            result = face_recognition(img_path, f)
            if result:
                return filename[:-4]
    return '?'

def main(port, model_name):
    model_selection_candidate = ['Fill_CNN', 'deepface', 'fer']
    model_selection = model_name
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', port))
    while True:
        response = s.recv(1024).decode()
        if response == 'quit':
            s.close()
            exit()
        if response == 'load_fer_model':
            try:
                if model_selection == 'Fill_CNN':
                    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                    model_path = 'fer_model/flicnn_model.keras'
                    model = keras.models.load_model(model_path, compile=False)
                    model.compile()
                elif model_selection == 'deepface':
                    _ = deep_face('./recordings/pictures/trump-2.jpg')
                elif model_selection == 'fer':
                    detector = FER()
                else:
                    pass
                s.sendall("fer_model_loaded".encode())
            except:
                s.sendall("fer_model_load_failed".encode())
        if response == 'run_fer_model':
            img = cv2.imread('./recordings/pictures/tmp_image.jpg')
            if model_selection == 'Fill_CNN':
                predict = self_trained_cnn(face_cascade, model, img)
            elif model_selection == 'deepface':
                predict = deep_face(img)
            elif model_selection == 'fer':
                predict = run_fer(img)
            else:
                predict = deep_face(img)
            # print(predict)
            # data = "predict: {}".format(predict)
            s.sendall(predict.encode())
        if response == 'face_recognition':
            name = recognition_from_data('./recordings/pictures/tmp_image.jpg', 'recordings/face_data')
            s.sendall(name.encode())

if __name__ == "__main__":
    # start = time.time()
    # deep_face()
    # deep_face_group_test()
    # self_trained_cnn_group_test()
    # fer_group_test()
    # face_region()
    # end = time.time()
    # print('Total Time used: {}'.format(end - start))
    main(int(sys.argv[1]), sys.argv[2])



    # deep_face('./recordings/face_data/jack.jpg')


    # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # model_path = './fer_model/flicnn_model.keras'
    # model = keras.models.load_model(model_path, compile=False)
    # model.compile()
    #
    # img = cv2.imread('./recordings/face_data/jack.jpg')
    #
    # predict = self_trained_cnn(face_cascade, model, img)
    # print(predict)
