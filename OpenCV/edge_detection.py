import cv2
import imutils
import numpy as np
import pytesseract


# Ouvre l'image
img = cv2.imread('dataset/AF54539.jpg')

# Redimensionnement de l'image pour une largeur de 800 pixels, maintien du rapport d'aspect
height, width = img.shape[:2]
new_width = 800
new_height = int((new_width / float(width)) * height)

# Redimensionner l'image
resized_img = cv2.resize(img, (new_width, new_height))

# Modification de l'image en ajoutant un filtre noir et blanc sur l'image
gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

# Application d'un flou bilatéral plus léger pour mieux capturer les détails
gray = cv2.bilateralFilter(gray, 5, 50, 50)  # Valeurs ajustées pour moins de flou
cv2.imwrite('results/gray.jpg', gray)

# Mise en évidence des contours de l'image avec des seuils plus adaptés
edged = cv2.Canny(gray, 10, 150)  # Ajustement des seuils pour plus de détails
cv2.imwrite('results/edged.jpg', edged)

# traitement à appliquer quand le edge trouve rien au screenCnt
# # Appliquer des transformations morphologiques pour améliorer la détection des contours
# kernel = np.ones((5, 5), np.uint8)  # Utiliser un noyau de taille 5x5 pour la dilatation et l'érosion

# # Dilatation pour renforcer les contours
# dilated = cv2.dilate(edged, kernel, iterations=1)

# # Erosion pour supprimer les petites irrégularités
# eroded = cv2.erode(dilated, kernel, iterations=1)

# cv2.imwrite('results/eroded.jpg', edged)

# Extraction des contours après le filtrage morphologique
contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)

# Filtrage des contours par taille (seulement ceux qui sont suffisamment grands)
contours = [c for c in contours if cv2.contourArea(c) > 100]

# Trier les contours par taille décroissante et prendre les 10 plus grands
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
screenCnt = None

# Dessiner les contours sur l'image redimensionnée
contour_img = resized_img.copy()
cv2.drawContours(contour_img, contours, -1, (255, 0, 0), 2)  # Dessiner en bleu
cv2.imwrite('results/all_contours.jpg', contour_img)

# Définition des dimensions approximatives des plaques européennes (en ratio largeur/hauteur)
PLATE_ASPECT_RATIO_MIN = 2.0
PLATE_ASPECT_RATIO_MAX = 6.0
screenCnt = None

# Recherche de contours correspondants aux plaques
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
output = resized_img.copy()

# Vérifie si un contour a été trouvé et le dessine
if screenCnt is not None:
    cv2.drawContours(output, [screenCnt], -1, (0, 255, 0), 3)

# Sauvegarde l'image avec la plaque détectée
cv2.imwrite('results/final_detection.jpg', output)

# Création du masque et extraction de la région d'intérêt
mask = np.zeros(gray.shape, dtype=np.uint8)  # Assurer que le masque est de type uint8

# Si une plaque a été trouvée, dessiner le contour sur le masque
if screenCnt is not None:
    mask = cv2.drawContours(mask, [screenCnt], -1, 255, thickness=cv2.FILLED)

    # Vérifier si le masque contient des pixels non nuls avant d'extraire la plaque
    if np.any(mask):  # Vérifie s'il y a des pixels blancs dans le masque
        # Extraction de la plaque
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx+1, topy:bottomy+1]

        # Sauvegarde la plaque extraite
        cv2.imwrite('results/cropped.jpg', Cropped)
    else:
        print("Aucune plaque détectée dans le masque.")
else:
    print("Aucune plaque détectée.")
