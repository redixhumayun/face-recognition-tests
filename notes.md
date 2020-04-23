## Notes On How Everything Works

This is a project that involves streaming video from the Raspberry Pi camera module to a server using sockets.

The server then performs face recognition on the video stream and outputs the name of the person in the stream.

The library used for performing facial recognition is [face_recognition](https://github.com/ageitgey/face_recognition).

The face_recognition library in turn depends on [dlib](http://dlib.net/) and (OpenCV)[https://opencv.org/].

The tutorial used for this example is [this](https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/).