import tkinter as tk
from tkinter import simpledialog, messagebox

class ConfigurationJeu(tk.Toplevel):
    def __init__(self, parent, lancer_jeu_callback):
        super().__init__(parent)
        self.lancer_jeu_callback = lancer_jeu_callback
        self.title("Configuration du jeu")
        self.geometry("400x450")

        # Choix du nombre de joueurs (maximum 4)
        self.label_nb_joueurs = tk.Label(self, text="Nombre de joueurs (max 4) :", font=("Helvetica", 14))
        self.label_nb_joueurs.pack(pady=10)
        self.var_nb_joueurs = tk.StringVar(value="2")
        self.menu_nb_joueurs = tk.OptionMenu(self, self.var_nb_joueurs, "2", "3", "4", command=self.mettre_a_jour_cartes)
        self.menu_nb_joueurs.pack(pady=5)

        # Choix des noms prédéfinis pour les joueurs
        self.label_noms_joueurs = tk.Label(self, text="Noms des joueurs :", font=("Helvetica", 14))
        self.label_noms_joueurs.pack(pady=10)


        self.noms_predifinis = ["L'analyste", "Le 9eme", "Jayas4", "Maccaud", "Les blattes d'Angel",  ]
        self.cadres_noms_joueurs = []
        for i in range(4):
            cadre = tk.Frame(self)
            cadre.pack(pady=5)
            label = tk.Label(cadre, text=f"Joueur {i+1} :")
            label.pack(side=tk.LEFT)
            var_nom = tk.StringVar(value=self.noms_predifinis[i])
            menu_noms = tk.OptionMenu(cadre, var_nom, *self.noms_predifinis)
            menu_noms.pack(side=tk.LEFT)
            self.cadres_noms_joueurs.append((cadre, var_nom))

        # Affichage du nombre de cartes (non modifiable)
        self.label_nb_cartes = tk.Label(self, text="Nombre de cartes :", font=("Helvetica", 14))
        self.label_nb_cartes.pack(pady=10)
        self.label_valeur_nb_cartes = tk.Label(self, text="48", font=("Helvetica", 14))
        self.label_valeur_nb_cartes.pack(pady=5)

        # Bouton pour lancer le jeu
        self.bouton_lancer = tk.Button(self, text="Lancer le jeu", command=self.lancer_jeu)
        self.bouton_lancer.pack(pady=20)

    def mettre_a_jour_cartes(self, nb_joueurs):
        if nb_joueurs == "2":
            self.label_valeur_nb_cartes.config(text="48")  # 24 paires
        elif nb_joueurs == "3" or nb_joueurs == "4":
            self.label_valeur_nb_cartes.config(text="48")  # 24 paires

    def lancer_jeu(self):
        nb_joueurs = int(self.var_nb_joueurs.get())
        noms_joueurs = [var_nom.get() for _, var_nom in self.cadres_noms_joueurs][:nb_joueurs]
        nb_cartes = int(self.label_valeur_nb_cartes.cget("text"))  # Utilisation correcte de cget pour récupérer le texte du label
        self.lancer_jeu_callback(nb_joueurs, noms_joueurs, nb_cartes)
        self.destroy()