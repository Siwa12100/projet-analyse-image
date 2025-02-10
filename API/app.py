import os
import cv2
from src.extract_text import extract_text_from_image
import imutils
import numpy as np
from src.process_image import process_image
from constants.parameters import *
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/detect', methods=['POST'])
def detect_image():
    """
    Route Flask pour l'upload et le traitement d'une image afin d'extraire le texte d'une plaque d'immatriculation.

    Méthode:
    --------
    POST

    Paramètres:
    -----------
    - file : fichier image (JPEG, PNG, etc.), envoyé via un formulaire multipart.

    Retour:
    -------
    - 200 OK : Si l'image est traitée avec succès.
      ```json
      {
          "message": "Image processed successfully",
          "license_plate": "ABC123"
      }
      ```
    - 400 Bad Request : En cas d'erreur (fichier manquant, mauvais format, etc.).
      ```json
      {
          "error": "No file part"
      }
      ```
    
    Description:
    ------------
    1. Vérifie si un fichier est présent dans la requête.
    2. Vérifie si le fichier a un nom valide.
    3. Vérifie si l'extension du fichier est autorisée (via `allowed_file`).
    4. Sauvegarde le fichier dans le dossier défini par `UPLOAD_FOLDER`.
    5. Passe le fichier à la fonction `process_image` pour détecter la plaque et extraire son texte.
    6. Retourne le texte extrait sous forme de réponse JSON.
    
    Exceptions:
    -----------
    - Retourne une erreur 400 si aucun fichier n'est fourni, si le fichier est vide, ou si son format est invalide.
    """

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Traiter l'image
        extracted_text = process_image(filepath)

        
        return jsonify({
            'message': 'Image processed successfully',
            'license_plate': extracted_text
        })
    else:
        return jsonify({'error': 'Invalid file format'}), 400

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(RESULTS_FOLDER):
        os.makedirs(RESULTS_FOLDER)

    app.run(debug=True)
