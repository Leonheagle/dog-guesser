# Dog Guesser

Dog Guesser est un jeu de quiz développé en Python. Le joueur doit identifier la race d'un chien à partir d'une image, en choisissant parmi quatre propositions. Une partie comporte 10 questions et le score final est enregistré par le serveur.

## Fonctionnalités

- Récupération des races et des images depuis l'API [Dog CEO](https://dog.ceo/dog-api/).
- Interface graphique réalisée avec Tkinter.
- Communication entre le client et le serveur avec WebSockets.
- Calcul et sauvegarde des scores dans un fichier texte.
- Possibilité de rejouer avec un autre pseudo.

## Prérequis

- Python 3.
- Une connexion Internet.
- Tkinter disponible dans l'installation de Python.

## Installation

Clonez le dépôt, puis ouvrez un terminal dans le dossier du projet :

```bash
git clone [URL_DU_DEPOT](https://github.com/Leonheagle/dog-guesser)
cd dog_guesser
```

Créez et activez un environnement virtuel.

Sous Windows :

```bash
python -m venv .venv
.venv\Scripts\activate
```

Installez les dépendances :

```bash
python -m pip install -r requirements.txt
```

## Lancement

Ouvrez deux terminaux dans le dossier du projet et activez l'environnement virtuel dans chacun.

**Terminal 1 — Serveur :**

```bash
python server.py
```

**Terminal 2 — Client :**

```bash
python client.py
```

Saisissez un pseudo puis cliquer sur le bouton commencer une partie.

## Structure du projet

- `client.py` : interface graphique et déroulement du quiz.
- `server.py` : communication WebSocket, gestion du score et sauvegarde des résultats.
- `dog_api.py` : récupération des races, des images et génération des questions.
- `requirements.txt` : dépendances nécessaires au projet.

Les scores sont enregistrés dans `scores.txt`, dans le dossier du serveur.

## Technologies utilisées

Python, Tkinter, Requests, Pillow, WebSockets et Dog CEO API.
