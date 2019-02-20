import cv2
import face_recognition
import argparse
import time
import os

#Set up accepting command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True, help="associate a name with the face")
ap.add_argument("-o", "--output", required=True, help="path to the output directory")
args = vars(ap.parse_args())

video_capture = cv2.VideoCapture(0)
total = 0

output_path = "./{}/{}".format(args["output"], args["name"])

#Create the file if it doesn't already exist
try:
  os.mkdir(output_path)
except FileExistsError as e:
  print(e)

#Loop over the video feed and capture the frame if user presses the key 'k'
while True:
  ret, frame = video_capture.read()
  orig = frame.copy()

  #Get face location in the image and draw a rectangle around it
  face_location = face_recognition.face_locations(frame)
  for(top, right, bottom, left) in face_location:
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

  cv2.imshow('Video', frame)

  key = cv2.waitKey(1) & 0xFF

  if key == ord("k"):
    # Set up path to the output directory
    p = os.path.sep.join([output_path, "{}.png".format(
			str(total).zfill(5))])
    cv2.imwrite(p, orig)
    total += 1


  elif key == ord("q"):
    break
  
#Once done, print number of images stored and destroy all cv2 windows
print("[INFO] {} face images stored".format(total))
cv2.destroyAllWindows()