import tkinter as tk
from tkinter import messagebox
import os
from titre import EcranTitre
from solo import Solo
from multi import Multijoueur
from configuration import ConfigurationJeu

root = tk.Tk()
root.title("Jeu de Memory")
root.resizable(False, False)

# Taille de l'écran titre
taille_ecran_titre = "731x700"
root.geometry(taille_ecran_titre)

niveau_difficulte = {
    "Facile": {"paires": 9, "temps": 60, "taille": "480x560"},
    "Normal": {"paires": 15, "temps": 120, "taille": "480x660"},
    "Difficile": {"paires": 24, "temps": 240, "taille": "480x800"},
}

# Fonction pour afficher l'écran titre
def afficher_ecran_titre():
    root.geometry(taille_ecran_titre)
    ecran_titre.grid(row=0, column=0, sticky="nsew")

# Fonction pour démarrer le jeu
def commencer(mode, difficulte):
    if mode == "Solo":
        lancer_jeu(mode, difficulte, 1, ["Joueur"], niveau_difficulte[difficulte]["paires"])
    elif mode == "Multijoueur":
        config_jeu = ConfigurationJeu(root, lambda nb_joueurs, noms_joueurs, nb_cartes: lancer_jeu(mode, difficulte, nb_joueurs, noms_joueurs, nb_cartes))

def lancer_jeu(mode, difficulte, nb_joueurs, noms_joueurs, nb_cartes):
    root.geometry(niveau_difficulte[difficulte]["taille"])
    if mode == "Solo":
        Solo(root, difficulte, niveau_difficulte, ecran_titre, afficher_ecran_titre, niveau_difficulte[difficulte]["paires"])
    elif mode == "Multijoueur":
        Multijoueur(root, nb_joueurs, noms_joueurs, ecran_titre, afficher_ecran_titre)
    ecran_titre.grid_remove()

# Créer et afficher l'écran titre
ecran_titre = EcranTitre(root, commencer)
ecran_titre.grid(row=0, column=0, sticky="nsew")

# Lance la boucle principale
root.mainloop()
