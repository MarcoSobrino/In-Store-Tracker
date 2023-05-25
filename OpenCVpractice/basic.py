import cv2 as cv

img = cv.imread('OpenCVpractice\\Photos\\school.jpg')

cv.imshow('School', img)
###
#converting to grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)

#blur
blur = cv.GaussianBlur(img, (7,7), cv.BORDER_DEFAULT)
cv.imshow('Blur', blur)

#edge cascade
canny = cv.Canny(img, 125, 175)
cv.imshow('Canny Edges', canny)

#dilating the image
dilated = cv.dilate(canny, (3,3), iterations=1)
cv.imshow('Dilated', dilated)


cv.waitKey(0)