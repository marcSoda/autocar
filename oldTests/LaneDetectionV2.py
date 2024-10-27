import cv2
import numpy as np
# version 2

# this code performs edge detection in real time from the webcam


def cannify(image): #edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # cvt to greyscale
    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # blur image (make softer)
    canny = cv2.Canny(blur, 50, 150)  # only show edges
    return canny


def displayLines(image, lines):
    lineImage = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            if line is not None:
                x1, y1, x2, y2 = line.reshape(4)
                cv2.line(lineImage, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return lineImage

###########################each point is a tuple (x and y val)
def regionOfInterest(image, point1, point2, point3, point4): #black out all pixels outside the region of interest (CHANGE AREA WHEN CAMERA IS MOUNTED)
    height = image.shape[0] #perhaps make this global so the calculaton isnt done every frame
    regionCoordinates = np.array([[point1, point2, point3, point4]]) #region of interest is a triangle, array of coordinates. all values from video
    mask = np.zeros_like(image) #array of zeros with dimensions like image
    cv2.fillPoly(mask, regionCoordinates, 255) #draw a white triangle corresponding to the region of interest
    maskedImage = cv2.bitwise_and(image, mask)
    return maskedImage

cap2 = cv2.VideoCapture("samples/curveTest.mp4")
cap = cv2.VideoCapture("samples/drivingVideo.mp4")
while cap.isOpened():
    _, frame = cap.read() #read video
    cannyImage = cannify(frame)  # edge detection
    croppedImage = regionOfInterest(cannyImage, (250, 720), (530, 280), (590, 280), (1020, 720))  # black out all pixels outside the region of interest
    laneLines = cv2.HoughLinesP(croppedImage, 2, np.pi / 180, 150, np.array([]), 40, 5)  # array of lane lines
    laneLineImage = displayLines(frame, laneLines)  # just the lane lines
    comboImage = cv2.addWeighted(frame, .8, laneLineImage, 1, 1)  # overlay lane lines onto original frame
    cv2.imshow("test", comboImage)  # show image

    _, frame2 = cap2.read()  # read video
    cannyImage2 = cannify(frame2)  # edge detection
    croppedImage2 = regionOfInterest(cannyImage2, (250, 660), (550, 420), (750, 420), (1100, 660))  # black out all pixels outside the region of interest
    laneLines2 = cv2.HoughLinesP(croppedImage2, 2, np.pi / 180, 150, np.array([]), 40, 5)  # array of lane lines
    laneLineImage2 = displayLines(frame2, laneLines2)  # just the lane lines
    comboImage2 = cv2.addWeighted(frame2, .8, laneLineImage2, 1, 1)  # overlay lane lines onto original frame
    cv2.imshow("test2", comboImage2)  # show image

    if cv2.waitKey(1) == ord('q'): break #break if 'q' pressed

cap.release()
cv2.destroyAllWindows()
