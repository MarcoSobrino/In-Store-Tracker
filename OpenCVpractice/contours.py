import cv2 as cv
import numpy as np

img = cv.imread('Photos\GroupPhoto.jpg')
#cv.imshow('GroupPhoto', img)


def rescaleFrame(frame, scale=0.5):
    # Images, Videos and Live Video
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

new_img = rescaleFrame(img)
#cv.imshow('Resized Image', resized_image)

blank = np.zeros(new_img.shape[:2], dtype='uint8')
cv.imshow('Blank', blank)

gray = cv.cvtColor(new_img, cv.COLOR_BGR2GRAY)
#cv.imshow('Gray', gray)

blur = cv.GaussianBlur(new_img, (5,5), cv.BORDER_DEFAULT)
cv.imshow('Blur', blur)

canny = cv.Canny(blur, 125, 175)
cv.imshow('Canny Edges', canny)

#ret, thresh = cv.threshold(gray, 125, 255, cv.THRESH_BINARY)
#cv.imshow('Thresh', thresh)

contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
print(f'{len(contours)} contour(s) found!')

cv.drawContours(blank, contours, -1, (0,0,255), 1)
cv.imshow('Contours Drawn', blank)

cv.waitKey(0)