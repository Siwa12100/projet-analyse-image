import cv2
import imutils
import numpy as np
import pytesseract
from constants.parameters import *
import os


def process_image(image_path):
    # Ouvre l'image
    img = cv2.imread(image_path)

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
    cv2.imwrite(os.path.join(RESULTS_FOLDER, 'gray.jpg'), gray)

    # Mise en évidence des contours de l'image avec des seuils plus adaptés
    edged = cv2.Canny(gray, 10, 150)  # Ajustement des seuils pour plus de détails
    cv2.imwrite(os.path.join(RESULTS_FOLDER, 'edged.jpg'), edged)

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
    cv2.imwrite(os.path.join(RESULTS_FOLDER, 'all_contours.jpg'), contour_img)

    # Définition des dimensions approximatives des plaques européennes (en ratio largeur/hauteur)
    PLATE_ASPECT_RATIO_MIN = 2.0
    PLATE_ASPECT_RATIO_MAX = 6.0
    screenCnt = None

    # Recherche de contours correspondants aux plaques
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.05 * peri, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            if 1000 < w * h < 10000 and PLATE_ASPECT_RATIO_MIN <= aspect_ratio <= PLATE_ASPECT_RATIO_MAX:
                screenCnt = approx
                break

    # Si aucune plaque n'a été détectée, appliquer des transformations morphologiques
    if screenCnt is None:
        kernel = np.ones((5, 5), np.uint8)

        # Dilatation pour renforcer les contours
        dilated = cv2.dilate(edged, kernel, iterations=1)

        # Erosion pour supprimer les petites irrégularités
        eroded = cv2.erode(dilated, kernel, iterations=1)

        # Extraction des contours après transformation
        contours = cv2.findContours(eroded.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        contours = [c for c in contours if cv2.contourArea(c) > 100]
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.05 * peri, True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = w / float(h)
                if 1000 < w * h < 10000 and PLATE_ASPECT_RATIO_MIN <= aspect_ratio <= PLATE_ASPECT_RATIO_MAX:
                    screenCnt = approx
                    break

    output = resized_img.copy()

    # Vérifie si un contour a été trouvé et le dessine
    if screenCnt is not None:
        cv2.drawContours(output, [screenCnt], -1, (0, 255, 0), 3)

    # Sauvegarde l'image avec la plaque détectée
    output_path = os.path.join(RESULTS_FOLDER, 'final_detection.jpg')
    cv2.imwrite(output_path, output)

    # Création du masque et extraction de la région d'intérêt
    mask = np.zeros(gray.shape, dtype=np.uint8)

    if screenCnt is not None:
        mask = cv2.drawContours(mask, [screenCnt], -1, 255, thickness=cv2.FILLED)
        if np.any(mask):  # Vérifie s'il y a des pixels blancs dans le masque
            (x, y) = np.where(mask == 255)
            (topx, topy) = (np.min(x), np.min(y))
            (bottomx, bottomy) = (np.max(x), np.max(y))
            Cropped = gray[topx:bottomx+1, topy:bottomy+1]
            cropped_path = os.path.join(RESULTS_FOLDER, 'cropped.jpg')
            cv2.imwrite(cropped_path, Cropped)
            cropped_text = pytesseract.image_to_string(Cropped, config='--psm 7')
        else:
            print("Aucune plaque détectée dans le masque.")
    else:
        print("Aucune plaque détectée.")

    return cropped_text