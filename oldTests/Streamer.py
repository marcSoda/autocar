import cv2
import sys
import socketserver
import numpy as np


class VideoStreamHandler(socketserver.StreamRequestHandler):
    def handle(self):
        stream_bytes = b' '

        try:
            # stream video frames one by one
            while True:
                stream_bytes += self.rfile.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    # stream_bytes = stream_bytes[last + 2:]
                    gray = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

                    # lower half of the image
                    height, width = gray.shape

                    cv2.imshow('image', gray)

                    # reshape image
                    # image_array = roi.reshape(1, int(height / 2) * width).astype(np.float32)
        finally:
            cv2.destroyAllWindows()
            sys.exit()


class Server(object):
    def __init__(self, host, port1):
        self.host = host
        self.port1 = port1

    def video_stream(self, host, port):
        s = socketserver.TCPServer((host, port), VideoStreamHandler)
        s.serve_forever()

    def start(self):
        self.video_stream(self.host, self.port1)


if __name__ == '__main__':
    # h, p1, p2 = "192.168.1.100", 8000, 8002
    h, p1 = "10.78.1.196", 8000

    ts = Server(h, p1)
    ts.start()
