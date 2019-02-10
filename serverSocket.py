import io
import socket
import struct
from PIL import Image
import numpy as np
import cv2
import face_recognition

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

    if process_this_frame:
      face_locations = face_recognition.face_locations(img)

    process_this_frame = not process_this_frame
    
    for (top, right, bottom, left) in face_locations:
      cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

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