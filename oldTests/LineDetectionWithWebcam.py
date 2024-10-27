import cv2
import numpy as np


# this code performs edge detection in real time from the webcam
def makeCoordinates(image, slope, intercept):
    if (slope is not None) and (intercept is not None):
        y1 = image.shape[0]
        y2 = int(y1 * (3/5))
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
        return np.array([x1, y1, x2, y2])
    else: return None #POSSIBLY STORE THE LAST LINE IN MEMORY AND SHOW IT IN THIS CASE
#       !!!!!!!!!!!!!!!!BETTERYET COMPUTE AN AVERAGE SLOPE AND INTERCEPT OVER THE PAST FEW FRAMES AND DISPLAY!!!!!!!!!!!!!!!!!!


def averageSlopeIntercept(image, lines):
    leftSlopes = []
    leftIntercepts = []
    rightSlopes = []
    rightIntercepts = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            if slope <= 0:
                leftSlopes.append(slope)
                leftIntercepts.append(intercept)
            else:
                rightSlopes.append(slope)
                rightIntercepts.append(intercept)

    if leftSlopes and leftIntercepts:
        leftSlopeAverage = np.nanmean(leftSlopes)
        leftInterceptAverage = np.nanmean(leftIntercepts)
    else:
        leftSlopeAverage = None
        leftInterceptAverage = None

    if rightSlopes and rightIntercepts:
        rightSlopeAverage = np.nanmean(rightSlopes)
        rightInterceptAverage = np.nanmean(rightIntercepts)
    else:
        rightSlopeAverage = None
        rightInterceptAverage = None

    leftLine = makeCoordinates(image, leftSlopeAverage, leftInterceptAverage)
    rightLine = makeCoordinates(image, rightSlopeAverage, rightInterceptAverage)
    return np.array([leftLine, rightLine])


def cannify(image): #edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # cvt to greyscale
    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # blur image (make softer)
    canny = cv2.Canny(blur, 50, 100)  # only show edges
    return canny


def displayLines(image, lines):
    lineImage = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            if line is not None:
                try:
                    x1, y1, x2, y2 = line.reshape(4)
                    cv2.line(lineImage, (x1, y1), (x2, y2), (255, 0, 0), 10)
                except: break
    return lineImage


def regionOfInterest(image): #black out all pixels outside the region of interest (CHANGE AREA WHEN CAMERA IS MOUNTED)
    height = image.shape[0] #perhaps make this global so the calculaton isnt done every frame
    triangle = np.array([[(200, height), (1100, height), (550, 250)]]) #region of interest is a triangle, array of coordinates. all values from video
    mask = np.zeros_like(image) #array of zeros with dimensions like image
    cv2.fillPoly(mask, triangle, 255) #draw a white triangle corresponding to the region of interest
    maskedImage = cv2.bitwise_and(image, mask)
    return maskedImage


cam = cv2.VideoCapture(0)  # initialize webcam (resolution is 640 x 480)
cv2.namedWindow("test")  # name window
while True:  # loop
    return_val, frame = cam.read()  # read webcam frames
    frameCopy = np.copy(frame)  # copy each frame
    cannyImage = cannify(frameCopy) #edge detection
    croppedImage = regionOfInterest(cannyImage) #black out all pixels outside the region of interest
    laneLines = cv2.HoughLinesP(croppedImage, 2, np.pi/180, 100, np.array([]), 40, 5) #array of lane lines
    averagedLines = averageSlopeIntercept(frameCopy, laneLines)
    laneLineImage = displayLines(frameCopy, averagedLines) #just the lane lines
    comboImage = cv2.addWeighted(frameCopy, .8, laneLineImage, 1, 1) #overlay lane lines onto original frame
    cv2.imshow("test", comboImage)  # show image
    # exit when escape pressed
    k = cv2.waitKey(1)
    if k % 256 == 27:
        break
cam.release()  # close camera
cv2.destroyAllWindows()  # close windows
