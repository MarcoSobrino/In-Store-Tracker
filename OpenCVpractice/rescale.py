import cv2 as cv

img = cv.imread('Photos\GroupPhoto.jpg')
#cv.imshow('GroupPhoto', img)

def rescaleFrame(frame, scale=0.5):
    # Images, Videos and Live Video
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

resized_image = rescaleFrame(img)
cv.imshow('Resized Image', resized_image)


cv.waitKey(0)