import io
import socket
import struct
import cv2
import numpy as np


class Server:  # host server runs on pc
    opened = False  # server open or not (used as loop constraint)
    address = ''  # ip address of host
    port = 0  # port
    clientSocket = None  # the socket of connected client
    binImgData = None  # file for image data received from socket
    serverSocket = None  # this socket

    def __init__(self, address, port):  # obj args are address and port
        self.address = address
        self.port = port

    def connect(self):  # connect client to server
        try:  # try to start socket
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # initialize socket
            self.serverSocket.bind((self.address, self.port))  # bind socket ip and port
            print("Server: Opened and awaiting stream")
        except:
            print("Server: Failed to open StreamCollector")
        try:  # try to recieve client
            self.serverSocket.listen(0)  # listen for client
            self.clientSocket, address = self.serverSocket.accept()  # accept client
            self.binImgData = self.clientSocket.makefile('rb')  # file in which input stream is stored
            self.opened = True  # the server is now open
            print(f"Stream Initialized from {address}")
        except:
            self.close()  # close if fail
            print("Server: No stream was found")

    def getStreamImage(self):  # return a single image frame from the client
        img = None  # opencv image
        try:
            imageLen = struct.unpack('<L', self.binImgData.read(struct.calcsize('<L')))[0]  # unpack received frame
            imageStream = io.BytesIO()  # instantiate image stream
            imageStream.write(self.binImgData.read(imageLen))  # write
            imageStream.seek(0)  # rewind stream
            imageBytes = np.asarray(bytearray(imageStream.read()), dtype=np.uint8) #construct a byte array for the stream data
            img = cv2.imdecode(imageBytes, cv2.IMREAD_GRAYSCALE) #convert the numpy byte array to an opencv image
        except:
            self.close() #close if fail
            print("Server: Stream halted")
            return None
        return img

    def sendCommand(self, command):
        self.clientSocket.send(bytes(command, "ascii"))

    def close(self): #close the server
        try:
            if self.clientSocket is not None:
                self.clientSocket.close()
            if self.binImgData is not None:
                self.binImgData.close()
            self.serverSocket.close()
            self.opened = False
            print("Server: Closed")
        except:
            print("Server: Failed to close")

    def isOpened(self): #loop constraint
        return self.opened


if __name__ == '__main__': #isolate server.py
    host, port = '10.78.1.195', 8000
    server = Server(host, port)
    server.connect()
    while server.isOpened():
        img = server.getStreamImage()
        cv2.imshow("stream", img)
        server.sendCommand("A")
        if cv2.waitKey(1) == ord('q'): server.close()
