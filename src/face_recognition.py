# import tensorflow as tf
# print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
from deepface import DeepFace

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

img1_path = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/recordings\pictures/happy\image1.jpg'
img2_path = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/recordings\pictures/happy\image3.jpg'
img_ex_path = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/recordings\pictures/happy\example.jfif'
img_db_path = 'D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src/recordings\pictures/happy'
result = DeepFace.verify(img1_path=img1_path, img2_path=img_ex_path)
print(result)

# dfs = DeepFace.find(img_path = img1_path, db_path = img_db_path)
# print(dfs)