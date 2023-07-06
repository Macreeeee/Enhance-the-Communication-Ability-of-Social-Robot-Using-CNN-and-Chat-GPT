from tensorflow import keras
import cv2
import numpy as np

# TODO: need to add a face region detection function.
path = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/fer_model/flicnn_model.keras'

model = keras.models.load_model(path, compile=False)
model.compile()
image = cv2.imread('./recordings/pictures/image1688649567.46.jpg')
h = 480
w = 640
image = image[w//2-24:w//2+24, h//2-24:h//2+24]
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('Image', image)
cv2.waitKey(0)
print('Resized Dimensions : ', image.shape)
predict = model.predict(np.array([image]))

print(predict)