# import tensorflow as tf
# print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
from deepface import DeepFace
import time

models = [
  "VGG-Face",
  "Facenet",
  "Facenet512",
  "OpenFace",
  "DeepFace",
  "DeepID",
  "ArcFace",
  "Dlib",
  "SFace",
]

img1_path = 'recordings/pictures/tmp_image.jpg'
img2_path = 'recordings/face_data/jack.jpg'
img_ex_path = 'recordings\pictures/happy\example.jfif'
img_db_path = 'recordings\pictures/happy'
result = DeepFace.verify(img1_path=img1_path, img2_path=img2_path)
start = time.time()
result = DeepFace.verify(img1_path=img1_path, img2_path=img2_path)
end = time.time()
print(end-start)
print(result)

# dfs = DeepFace.find(img_path = img1_path, db_path = img_db_path)
# print(dfs)