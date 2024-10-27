from MotorController import MotorController
from Client import Client
import threading

motors = MotorController() #inisialize motor controller
#ONLY RUNS IN SECOND THREAD
def getMessage():
    while motors.areRunning():
        message = client.receiveInstruction() #get command from server
        if message == 'w':
            motors.forward()
        elif message == 'a':
            motors.left()
        elif message == 'd':
            motors.right()
        elif message == 's':
            motors.stop()
        elif message == 'q': #KILL ALL THREADS AND PROCESSES
            motors.exit()
            client.close()
            messageThread._is_running = False
######


host, port = '10.78.1.195', 8000 #home
#host, port = '172.20.10.3', 8000 #marcantonio
client = Client(host, port) #initialize this socket
client.connect() #connect to the server
# client.initCamera((300,300), 15)
client.initCamera((550,150), 10) #initialize the camera with a size of 550 x 150 at 10 fps

#START SECOND THREAD
messageThread = threading.Thread(target=getMessage)
messageThread.start()
######

while client.isConnected():
    client.sendStreamImage()
