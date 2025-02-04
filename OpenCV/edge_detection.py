import cv2
import imutils
import numpy as np

# Ouvre l'image
img = cv2.imread('dataset/car.jpg')

# Modification de l'image en ajoutant un filtre noir et blanc sur l'image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Ajout d'un filtre qui floute le background pour laisser la voiture en net
gray = cv2.bilateralFilter(gray, 13, 15, 15)

cv2.imwrite('results/gray.jpg', gray)


# Mise en évidence des contours de l'image
edged = cv2.Canny(gray, 30, 200)

cv2.imwrite('results/edged.jpg', edged)



contours=cv2.findContours(edged.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
contours = sorted(contours,key=cv2.contourArea, reverse = True)[:10]
screenCnt = None

for c in contours:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * peri, True)
    # if our approximated contour has four points, then
    # we can assume that we have found our screen
    if len(approx) == 4:
        screenCnt = approx
        break

mask = np.zeros(gray.shape,np.uint8)
new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
new_image = cv2.bitwise_and(img,img,mask=mask)

(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
Cropped = gray[topx:bottomx+1, topy:bottomy+1]


cv2.imwrite('results/cropped.jpg', Cropped)