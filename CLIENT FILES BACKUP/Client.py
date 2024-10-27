import io
import socket
import struct
import time
import picamera

class Client: #client runs on raspberry pi
    connected = False #client connected or not (used as loop constraint)
    serverAddress = '' #the address of the server PC to connect to (NOT THE PI)
    port = 0 #port must be same as server PC
    serverSocket = None #the server hosted on PC
    binImgData = None #image data
    clientSocket = None #this socket
    stream = None #image stream
    camera = None #picamera state data

    def __init__(self, serverAddress, port):
        self.serverAddress = serverAddress
        self.port = port

    def connect(self): #connect to server
        try:
            self.stream = io.BytesIO() #initialize image stream
            self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #initialize client
            self.clientSocket.connect((self.serverAddress, self.port)) #connect to server
            self.binImgData = self.clientSocket.makefile('wb') #image data file
            self.connected = True #client is now connected
            print("Client: Succussfully connected to server")
        except:
            print("Client: Failed to connect to server")
            self.close

    def initCamera(self, resolution, framerate): #initialize the camera
        try:
            self.camera = picamera.PiCamera() #instantiate camera
            self.camera.vflip = True #vertical flip image
            self.camera.hflip = True #horizontal flip image
            self.camera.resolution = resolution #camera resolution argument tuple
            self.camera.framerate = framerate #camera framerate argument
            print("Client: Camera succussfully initialized")
        except:
            print("Client: Failed to initialize camera")
            self.close()

    def sendStreamImage(self): #send stream image to server
        try:
            self.camera.capture(self.stream, 'jpeg', use_video_port=True) #capture frame to stream
            self.binImgData.write(struct.pack('<L', self.stream.tell())) #write the length of the capture to the stream
            self.binImgData.flush() #send and clear buffer (ensure length gets sent)
            self.stream.seek(0) #rewind stream
            self.binImgData.write(self.stream.read()) #send stream to server
            self.stream.seek(0) #rewind stream
            self.stream.truncate() #reset stream for next capture
        except:
            print("Client: Stream halted")
            self.close()

    def receiveInstruction(self): #recieve an instruction from the server
        return self.clientSocket.recv(1).decode("ascii") #return decoded instruction

    def close(self):
        self.connected = False
        print("Client: Closed")

    def isConnected(self): #loop constraint
        return self.connected

if __name__ == "__main__": #isolate client.py
    host, port = '10.78.1.195', 8000 #home
    client = Client(host, port)
    client.connect()
    client.initCamera((320,240), 10)
    while client.isConnected():
        client.sendStreamImage()
        msg = client.receiveInstruction()
        # if msg is not None:
        #     print(msg.decode("ascii"))
