import io
import socket
import struct
import cv2
import numpy as np


class StreamCollectorV3:
    isOpened = False
    address = ''
    port = 0
    connection = None
    socketServer = socket.socket()

    def __init__(self, address, port):
        self.address = address
        self.port = port

    def connect(self):
        try:
            self.socketServer = socket.socket()
            self.socketServer.bind((self.address, self.port))  # ADD IP HERE
            print("StreamCollector: Opened and awaiting stream")
        except: print("StreamCollector: Failed to open StreamCollector")
        try:
            self.socketServer.listen(0)
            self.connection = self.socketServer.accept()[0].makefile('rb')
            print("StreamCollector: Stream Initialized")
            self.isOpened = True
        except:
            self.close()
            print("StreamCollector: No stream was found")

    def getStreamImage(self):
        img = None
        try:
            image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
            imageStream = io.BytesIO()
            imageStream.write(self.connection.read(image_len))
            imageStream.seek(0)
            imageBytes = np.asarray(bytearray(imageStream.read()), dtype=np.uint8)
            img = cv2.imdecode(imageBytes, cv2.IMREAD_GRAYSCALE)
        except:
            self.close()
            print("StreamCollector: Stream halted")
        return img

    def close(self):
        try:
            if self.connection is not None:
                self.connection.close()
            self.socketServer.close()
            self.isOpened = False
            print("StreamCollector: Closed")
        except: print("StreamCollector: Failed to close")

    def isOpened(self):
        return self.isOpened


if __name__ == '__main__':
    host, port = '10.78.1.195', 8000
    stream = StreamCollectorV3(host, port)
    stream.connect()
    while stream.isOpened:
        img = stream.getStreamImage()
        cv2.imshow("stream", img)
        if cv2.waitKey(1) == ord('q'): stream.close()
