import io
import socket
import struct
import numpy as np
import cv2
import face_recognition
import pickle


# Start a socket listening for connections on 0.0.0.0:8080 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8080))
server_socket.listen(0)

clientsocket, address = server_socket.accept()
connection = clientsocket.makefile('rb')

#Set up a window for cv2 to overwrite repeatedly
cv2.namedWindow('videoplayer', cv2.WINDOW_NORMAL)

#Global variable to determine whether to process this frame or not
process_this_frame = True

#Load the encoded face data which is part of our dataset
data = pickle.loads(open('./build', 'rb').read())

try:
  while True:
    image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
    if not image_len:
      break
    image_stream = io.BytesIO()
    image_stream.write(connection.read(image_len))
    image_stream.seek(0)
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if process_this_frame:
      face_locations = face_recognition.face_locations(img_rgb)
      face_encodings = face_recognition.face_encodings(img_rgb)

      for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(data['encodings'], face_encoding)
        name = "Unknown"

        matches_as_nparray = np.asarray(matches)
        if np.any(matches_as_nparray):
          match_indices = np.where(matches_as_nparray == True)
          first_match_index = match_indices[0][0]
          name = data['names'][first_match_index]

    process_this_frame = not process_this_frame
    
    for (top, right, bottom, left) in face_locations:
      # Draw box around the face
      cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

      # Draw a label with a name below the face
      cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
      font = cv2.FONT_HERSHEY_DUPLEX
      cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('videoplayer', img)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
      break

except Exception as e:
  print("Error", e)

finally:
  clientsocket.close()
  server_socket.close()
  cv2.destroyAllWindows()