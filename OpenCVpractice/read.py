import cv2 as cv

img = cv.imread('Photos\school.jpg')

cv.imshow('School', img)

cv.waitKey(0)