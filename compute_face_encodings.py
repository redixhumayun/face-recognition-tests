import os
import face_recognition
import cv2
import argparse
import pickle

#Set up accepting command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True, help="the file path to which the encodings should be written")
args = vars(ap.parse_args())

#Compute facial encodings for each of the files and write them to a file on disk
known_names = []
known_encodings = []

#Get all known faces and files associated with those faces first
constructed_path = os.path.join(os.getcwd() + '/faces_dataset')
image_paths = []
for root, dirs, files in os.walk(constructed_path):
  image_paths = [root + '/' + filePath for filePath in files if filePath.endswith('.png')]

for image_path in image_paths:
  name = image_path.split(os.path.sep)[-2]
  image = cv2.imread(image_path)

  #Convert the image from BGR to RGB color space because dlib and face_recognition use RGB
  #while cv2 use BGR
  image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  face_location = face_recognition.face_locations(image_rgb)
  face_encoding = face_recognition.face_encodings(image_rgb)
  known_names.append(name)
  known_encodings.append(face_encoding)

data = {"encodings": known_encodings, "names": known_names}
f = open(args["output"], "wb")
f.write(pickle.dumps(data))
f.close()