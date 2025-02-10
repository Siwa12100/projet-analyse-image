import cv2
import imutils
import numpy as np


# Ouvre l'image
img = cv2.imread('dataset/renault-credit-renault.jpg')

height, width = img.shape[:2]
new_width = 800
new_height = int((new_width / float(width)) * height)

# Redimensionner l'image
resized_img = cv2.resize(img, (new_width, new_height))

# Modification de l'image en ajoutant un filtre noir et blanc sur l'image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Application d'un flou bilatéral plus doux pour mieux capturer les détails
gray = cv2.bilateralFilter(gray, 10, 75, 75)
cv2.imwrite('results/gray.jpg', gray)

# Mise en évidence des contours de l'image avec des seuils plus adaptés
edged = cv2.Canny(gray, 3, 100)
cv2.imwrite('results/edged.jpg', edged)


contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
screenCnt = None

contour_img = img.copy()
cv2.drawContours(contour_img, contours, -1, (255, 0, 0), 2)
cv2.imwrite('results/all_contours.jpg', contour_img)

# Définition des dimensions approximatives des plaques européennes (en ratio largeur/hauteur)
PLATE_ASPECT_RATIO_MIN = 3.0
PLATE_ASPECT_RATIO_MAX = 6.0

screenCnt = None

for c in contours:
    # Approximation du contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.05 * peri, True)  # Modification de l'approximation pour plus de flexibilité
    
    # Si le contour approximé a quatre points, on suppose qu'on a trouvé une plaque potentielle
    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)
        
        # Vérification de la taille du rectangle pour exclure les contours trop petits/grands
        if 1000 < w * h < 10000:  # Modifier la plage selon les dimensions de tes plaques
            # Vérification du ratio largeur/hauteur
            if PLATE_ASPECT_RATIO_MIN <= aspect_ratio <= PLATE_ASPECT_RATIO_MAX:
                screenCnt = approx
                break

# Copie de l'image originale pour afficher les boîtes détectées
output = img.copy()

# Vérifie si un contour a été trouvé et le dessine
if screenCnt is not None:
    cv2.drawContours(output, [screenCnt], -1, (0, 255, 0), 3)

# Sauvegarde l'image avec la plaque détectée
cv2.imwrite('results/final_detection.jpg', output)

# Création du masque et extraction de la région d'intérêt
mask = np.zeros(gray.shape, np.uint8)
if screenCnt is not None:
    new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    # Extraction de la plaque
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx+1, topy:bottomy+1]

    cv2.imwrite('results/cropped.jpg', Cropped)
