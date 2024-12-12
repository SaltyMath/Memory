import tkinter as tk
import os

class EcranTitre(tk.Frame):
    def __init__(self, master, lancer_jeu_callback):
        super().__init__(master)
        self.master = master
        self.lancer_jeu_callback = lancer_jeu_callback
        
        # Chemin du répertoire pour les fichiers de meilleurs temps dans le dossier "Scores"
        self.chemin_repertoire = os.path.join(os.path.dirname(__file__), "Scores")
        if not os.path.exists(self.chemin_repertoire):
            os.makedirs(self.chemin_repertoire)
        
        self.pack(fill="both", expand=True)

        self.mode_de_jeu = tk.StringVar(value="Solo")
        self.difficulte = tk.StringVar(value="Facile")
        self.creer_widgets()

    def creer_widgets(self):
        titre_label = tk.Label(self, text="Jeu de Memory", font=("Helvetica", 24))
        titre_label.pack(pady=20)

        mode_label = tk.Label(self, text="Choisissez le mode de jeu :", font=("Helvetica", 16))
        mode_label.pack(pady=10)

        modes = [("Solo", "Solo"), ("Multijoueur", "Multijoueur")]
        for text, mode in modes:
            tk.Radiobutton(self, text=text, variable=self.mode_de_jeu, value=mode).pack(pady=5)

        difficulte_label = tk.Label(self, text="Choisissez la difficulté (solo seulement):", font=("Helvetica", 16))
        difficulte_label.pack(pady=10)

        difficultes = [("Facile", "Facile"), ("Normal", "Normal"), ("Difficile", "Difficile")]
        for text, mode in difficultes:
            tk.Radiobutton(self, text=text, variable=self.difficulte, value=mode).pack(pady=5)

        bouton_commencer = tk.Button(self, text="Commencer le jeu", font=("Helvetica", 16), command=self.commencer_jeu)
        bouton_commencer.pack(pady=20)

        self.label_meilleurs_temps = tk.Label(self, text="Meilleurs temps :", font=("Helvetica", 16))
        self.label_meilleurs_temps.pack(pady=10)

        self.cadres_meilleurs_temps = {}
        self.listes_meilleurs_temps = {}

        for niveau in ["Facile", "Normal", "Difficile"]:
            cadre = tk.Frame(self)
            cadre.pack(side=tk.LEFT, padx=10)
            label = tk.Label(cadre, text=f"{niveau} :", font=("Helvetica", 14))
            label.pack(pady=5)
            liste = tk.Listbox(cadre, font=("Helvetica", 14))
            liste.pack()
            self.cadres_meilleurs_temps[niveau] = cadre
            self.listes_meilleurs_temps[niveau] = liste

        self.charger_meilleurs_temps()

    def commencer_jeu(self):
        self.pack_forget()
        self.lancer_jeu_callback(self.mode_de_jeu.get(), self.difficulte.get())

    def charger_meilleurs_temps(self):
        for niveau in ["Facile", "Normal", "Difficile"]:
            liste = self.listes_meilleurs_temps[niveau]
            liste.delete(0, tk.END)
            chemin_meilleurs_temps = os.path.join(self.chemin_repertoire, f"records_{niveau.lower()}.txt")
            meilleurs_temps = []
            if os.path.exists(chemin_meilleurs_temps):
                with open(chemin_meilleurs_temps, "r") as fichier:
                    meilleurs_temps = [line.strip() for line in fichier.readlines()]
            else:
                with open(chemin_meilleurs_temps, "w") as fichier:
                    pass

            for temps in meilleurs_temps:
                liste.insert(tk.END, temps)

    def sauvegarder_meilleur_temps(self, difficulte, nouveau_temps):
        chemin_meilleurs_temps = os.path.join(self.chemin_repertoire, f"records_{difficulte.lower()}.txt")
        meilleurs_temps = []
        if os.path.exists(chemin_meilleurs_temps):
            with open(chemin_meilleurs_temps, "r") as fichier:
                meilleurs_temps = [line.strip() for line in fichier.readlines()]

        # Ajout du nouveau temps
        meilleurs_temps.append(nouveau_temps)

        # Fonction pour extraire le temps en secondes à partir d'une entrée
        def extraire_temps(entree):
            try:
                return int(entree.split()[-2])
            except ValueError:
                return float('inf')

        # Tri des meilleurs temps et limitation aux 5 meilleurs
        meilleurs_temps = sorted(meilleurs_temps, key=extraire_temps)[:5]

        # Sauvegarde des meilleurs temps dans le fichier
        with open(chemin_meilleurs_temps, "w") as fichier:
            for temps in meilleurs_temps:
                fichier.write(temps + "\n")

        # Rechargement des meilleurs temps pour mettre à jour l'affichage
        self.charger_meilleurs_temps()


