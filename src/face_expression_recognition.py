from tensorflow import keras
import cv2
import numpy as np
import matplotlib.pyplot as plt
from deepface import DeepFace
import time
from PIL import Image
import io
import sys
import socket


def face_region(face_cascade, img):
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
    # for (x, y, w, h) in faces:
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    try:
        (x, y, w, h) = faces[0]
    except:
        print('no face region find')
        return img
    return img[y:y + h, x:x + w]


def self_trained_cnn(face_cascade, model, image):
    # image = cv2.imread(img_path)

    image = face_region(face_cascade, image)

    image = cv2.resize(image, (48, 48))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    predict = model.predict(np.array([image]))
    emotion_list = ['anger', 'disgust', 'happy', 'sad', 'surprise', 'neutral']
    predict = emotion_list[np.argmax(predict)]

    return predict


def self_trained_cnn_group_test():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    path = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/fer_model/flicnn_model.keras'
    model = keras.models.load_model(path, compile=False)
    model.compile()
    emotion_list = ['anger', 'disgust', 'happy', 'sad', 'surprise', 'neutral']
    # emotion_list = ['anger', 'neutral', 'sad', 'disgust', 'happy', 'surprise']
    emotion_folder_list = ['anger', 'disgust', 'sad', 'surprise', 'neutral']
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
            if prediction == e:
                count += 1
    print(count / total)


def deep_face():
    img = cv2.imread('./recordings/pictures/happy/image1.jpg')
    plt.imshow(img[:, :, :: -1])

    result = DeepFace.analyze(img, actions=['emotion'])
    print(result)

    x1 = int(result[0]['region']['x'])
    x2 = x1 + int(result[0]['region']['w'])
    y1 = int(result[0]['region']['y'])
    y2 = y1 + int(result[0]['region']['h'])
    plt.imshow(img[y1:y2, x1:x2, :: -1])
    plt.show()


def deep_face_group_test():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # emotion_list = ['happy']
    emotion_list = ['anger', 'disgust', 'happy', 'sad', 'surprise', 'neutral']
    count = 0
    total = 0
    for e in emotion_list:
        for i in range(10):
            total += 1
            img = cv2.imread('./recordings/pictures/{}/image{}.jpg'.format(e, str(i)))
            # img = face_region(face_cascade, img)
            try:
                result = DeepFace.analyze(img, actions=['emotion'])
                prediction = result[0]['dominant_emotion']
            except:
                prediction = 'None'
            print('true: {}, pre: {}'.format(e, prediction))
            if prediction == e:
                count += 1
    print(count / total)


if __name__ == "__main__":
    # start = time.time()
    # deep_face()
    # deep_face_group_test()
    # self_trained_cnn_group_test()
    # face_region()
    # end = time.time()
    # print('Total Time used: {}'.format(end - start))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 5000))
    while True:
        response = s.recv(1024).decode()
        if response == 'quit':
            s.close()
            exit()
        if response == 'load_fer_model':
            try:
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                model_path = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/fer_model/flicnn_model.keras'
                model = keras.models.load_model(model_path, compile=False)
                model.compile()
                s.sendall("fer_model_loaded".encode())
            except:
                s.sendall("fer_model_load_failed".encode())
        if response == 'run_fer_model':
            img = cv2.imread('./recordings/pictures/tmp_image.jpg')
            predict = self_trained_cnn(face_cascade, model, img)
            # print(predict)
            # data = "predict: {}".format(predict)
            s.sendall(predict.encode())

    # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # model_path = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/fer_model/flicnn_model.keras'
    # model = keras.models.load_model(model_path, compile=False)
    # model.compile()
    #
    # img = cv2.imread('./recordings/pictures/tmp_image.jpg')
    #
    # predict = self_trained_cnn(face_cascade, model, img)
    # print(predict)


