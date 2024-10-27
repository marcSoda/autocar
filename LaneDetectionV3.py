import cv2
import numpy as np


def getNNInput(grayscaleFrame):  # returns perspective transform. Maybe redo later to return polynomial coefficients of the curve
    blur = cv2.GaussianBlur(grayscaleFrame, (5, 5), 0)  # blur image (make softer)
    sobelImage = cv2.Sobel(blur, cv2.THRESH_BINARY, 1, 0)  # edge detection
    cannyImage = cv2.Canny(sobelImage, 100, 600)  # only show edges
    perspectiveTrans = perspectiveTransform(cannyImage)  # perspective transform
    return perspectiveTrans


def perspectiveTransform(img):  # convert car view to "bird's eye" view
    img_size = (img.shape[1], img.shape[0])  #
    # src = np.float32(  # scr points transform to dst points.
        # [[200, 720],
        #  [1100, 720],
        #  [595, 450],
        #  [685, 450]])
    src = np.float32(
        [[70, 150],
         [530, 150],
         [200, 40],
         [315, 40]])
    # dst = np.float32(  # scr points transform to dst points.
    #     [[300, 720],
    #      [980, 720],
    #      [300, 0],
    #      [980, 0]])
    dst = np.float32(
        [[70, 150],
         [530, 150],
         [70, 0],
         [530, 0]])

    m = cv2.getPerspectiveTransform(src, dst)  # coords for warp
    warped = cv2.warpPerspective(img, m, img_size, flags=cv2.INTER_LINEAR)  # warp entire image
    return warped


if __name__ == '__main__': #isolate LaneDetection
    cap = cv2.VideoCapture("samples/curveTest.mp4")
    while cap.isOpened():
        _, frame = cap.read()
        nnInput = getNNInput(frame)
        cv2.imshow("t", frame)  # show image
        cv2.imshow("tttttt", nnInput)  # show image
        if cv2.waitKey(1) == ord('q'): break  # break if 'q' pressed

    cap.release()
    cv2.destroyAllWindows()
