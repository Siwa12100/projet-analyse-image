
# Détection de plaque d'immatriculation

Notre projet effectue des traitements sur une image de voiture pour en retourner le texte de la plaque d'immatriculation.

# Guide d'utilisation

### Utiliser le projet

Le projet a été déployé sur un vps personnel de manière à faciliter son accès. Le panel web est ainsi accessible depuis http://149.7.5.30:21007, et l'API est elle accessible en http://149.7.5.30:21090. 

Attention si vous êtes à l'IUT, le proxy bloque les requêtes en http. Il faut simplement le désactiver dans les options du navigateur. 

### Prérequis

- Python3+
- Dernière version de PIP
- Docker / DockerDesktop

### Installation des dépendances Python
Vous devez juste executer ces 3 commandes :

```bash
git clone <URL du projet>
cd projet-analyse-image
pip install -r requirements.txt
```


### Lancer l'API
Pour lancer l'API :
```bash
cd API/
sh ./lancement-projet.sh
```
Vous aurez dans le terminal une log du port utilisé.

Pour arrêter l'API et supprimer l'image :
```bash
cd API/
sh ./arret.sh
sh ./supprimer-image.sh
```

### Lancer le Panel Web
Pour lancer le panel web :
```bash
cd API/
sh ./lancement-projet.sh
```
Vous aurez dans le terminal une log du port utilisé.

Pour arrêter l'API et supprimer l'image :
```bash
cd API/
sh ./arret.sh
sh ./supprimer-image.sh
```

### Documentation

Une documentation des fonctions est disponible pour les fonctions:
- process_image()
- detect_image()


# Auteurs

- [Antoine PINAGOT](https://github.com/YalIhow)
- [Jean MARCILLAC](https://github.com/Siwa12100)
