import cv2
import numpy as np
# version 1 just calculates two lane lines

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
    canny = cv2.Canny(blur, 50, 150)  # only show edges
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


###########################each point is a tuple (x and y val)
def regionOfInterest(image, point1, point2, point3, point4): #black out all pixels outside the region of interest (CHANGE AREA WHEN CAMERA IS MOUNTED)
    height = image.shape[0] #perhaps make this global so the calculaton isnt done every frame
    regionCoordinates = np.array([[point1, point2, point3, point4]]) #region of interest is a triangle, array of coordinates. all values from video
    mask = np.zeros_like(image) #array of zeros with dimensions like image
    cv2.fillPoly(mask, regionCoordinates, 255) #draw a white triangle corresponding to the region of interest
    maskedImage = cv2.bitwise_and(image, mask)
    return maskedImage

cap = cv2.VideoCapture("samples/curveTest.mp4")
while cap.isOpened():
    _, frame = cap.read() #read video
    cannyImage = cannify(frame)  # edge detection
    croppedImage = regionOfInterest(cannyImage, (250, 660), (550, 420), (750, 420), (1100, 660))  # black out all pixels outside the region of interest
    laneLines = cv2.HoughLinesP(croppedImage, 2, np.pi / 180, 250, np.array([]), 40, 5)  # array of lane lines (arguments open for optimization)
    averagedLines = averageSlopeIntercept(frame, laneLines) #two lane lines
    laneLineImage = displayLines(frame, averagedLines)  # just the lane lines
    comboImage = cv2.addWeighted(frame, .8, laneLineImage, 1, 1)  # overlay lane lines onto original frame
    cv2.imshow("test", comboImage)  # show image
    if cv2.waitKey(1) == ord('q'): break #break if 'q' pressed

cap.release()
cv2.destroyAllWindows()
