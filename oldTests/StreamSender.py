import io
import socket
import struct
import time
import picamera

# create socket and bind host
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('10.78.1.195', 8000))
binImgData = client_socket.makefile('wb')
stream = io.BytesIO()

try:
    camera = picamera.PiCamera()
    camera.resolution = (320, 240)  # pi camera resolution
    camera.framerate = 15  # 15 frames/sec

    for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
        binImgData.write(struct.pack('<L', stream.tell()))
        binImgData.flush()
        stream.seek(0)
        binImgData.write(stream.read())
        stream.seek(0)
        stream.truncate()

finally:
    binImgData.close()
    client_socket.close()
