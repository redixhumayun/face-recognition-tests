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

    cv2.imshow('Frame', img)
    cv2.waitKey()

    # image = Image.open(image_stream)
    # print('Image is %dx%d' % image.size)
    # image.verify()
    # print('Image is verified')
    # Image.open(image_stream).save('./random', format='jpeg')

    
except Exception as e:
  print("Error", e)
finally:
  clientsocket.close()
  server_socket.close()

# image = face_recognition.load_image_file('./random')
# face_locations = face_recognition.face_locations(image)

# for (top, right, bottom, left) in face_locations:
#   cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

# cv2.imshow('image', image)
# cv2.waitKey()