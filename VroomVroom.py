import cv2
from pynput import keyboard
from LaneDetectionV3 import getNNInput
from Server import Server


#ONLY RUNS IN KEYBOARD LISTENER THREAD
def keyPress(key):  # send keypress to client
    command = str(key)[1]
    if command == 'w' or command == 'a' or command == 'd' or command == 's' or command == 'q':
        server.sendCommand(command)
######


host, port = '10.78.1.195', 8000  # home
# host, port = '172.20.10.3', 8000 #marcantonio
server = Server(host, port)  # server objecta
server.connect()  # host the server and wait for a connection

######THIS INITIALIZES THE SECOND THREAD (keyboard listener)
listener = keyboard.Listener(on_press=keyPress)
listener.start()
######

while server.isOpened():  # do while the server is open
    frame = server.getStreamImage()  # get an image from the client each frame
    cv2.imshow("Frame", frame)  # show image

    nnInput = getNNInput(frame) # transform the frame
    cv2.imshow("Transformed Frame", nnInput)  # show image binary image of the perspective transformation of the lane lines

    if cv2.waitKey(1) == ord('q'):  # quit if q pressed
        server.close()  # break if 'q' pressed
        listener._is_running = False

cv2.destroyAllWindows()  # close opencv windows
