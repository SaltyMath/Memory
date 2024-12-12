import tkinter as tk
from tkinter import simpledialog, messagebox
import random

class Solo:
    def __init__(self, root, difficulte, niveau_difficulte, ecran_titre, afficher_ecran_titre, nb_cartes):
        self.root = root
        self.difficulte = difficulte
        self.niveau_difficulte = niveau_difficulte
        self.ecran_titre = ecran_titre
        self.afficher_ecran_titre = afficher_ecran_titre
        self.game_over = False
        self.temps_restant = niveau_difficulte[difficulte]["temps"]
        self.boutons = []
        self.cartes_revelees = []
        self.par_pair = [False] * (nb_cartes * 2)
        self.cartes = list(range(nb_cartes)) * 2
        random.shuffle(self.cartes)

        self.cadre_jeu = tk.Frame(root)
        self.label_timer = tk.Label(self.cadre_jeu, text=f"Temps restant: {self.temps_restant} secondes", font=("Helvetica", 16))
        self.label_timer.grid(row=0, column=0, columnspan=6)
        
        for i in range(nb_cartes * 2):
            bouton = tk.Button(self.cadre_jeu, text='', width=10, height=5, command=lambda i=i: self.on_bouton_click(i))
            bouton.grid(row=(i//6) + 1, column=i%6)
            self.boutons.append(bouton)
        
        self.image_victoire = tk.PhotoImage(file="./Memory/V2/ImgMp4/victory.png")
        self.label_victoire = tk.Label(self.cadre_jeu, image=self.image_victoire)
        
        self.image_defaite = tk.PhotoImage(file="./Memory/V2/ImgMp4/defeat.png")
        self.label_defaite = tk.Label(self.cadre_jeu, image=self.image_defaite)
        
        self.lancer_chrono()
        self.cadre_jeu.grid(row=0, column=0, sticky="nsew")

    def on_bouton_click(self, index):
        if self.game_over or len(self.cartes_revelees) == 2 or self.par_pair[index]:
            return

        self.boutons[index].config(text=self.cartes[index], state='disabled')
        self.cartes_revelees.append(index)

        if len(self.cartes_revelees) == 2:
            self.root.after(1000, self.verifier_paire)

    def verifier_paire(self):
        if self.cartes[self.cartes_revelees[0]] == self.cartes[self.cartes_revelees[1]]:
            self.par_pair[self.cartes_revelees[0]] = True
            self.par_pair[self.cartes_revelees[1]] = True
        else:
            for i in self.cartes_revelees:
                self.boutons[i].config(text='', state='normal')
        self.cartes_revelees = []

        if all(self.par_pair):
            self.game_over = True
            self.afficher_victoire()

    def afficher_victoire(self):
        self.label_victoire.grid(row=len(self.boutons)//6 + 2, column=0, columnspan=6, pady=10)
        nom_joueur = simpledialog.askstring("Nom du joueur", "Entrez votre nom:")
        if nom_joueur:
            nouveau_temps = f"{nom_joueur} {self.niveau_difficulte[self.difficulte]['temps'] - self.temps_restant} secondes"
            print(f"Enregistrement du temps: {nouveau_temps}")  # Message de débogage
            self.ecran_titre.sauvegarder_meilleur_temps(self.difficulte, nouveau_temps)
        self.root.after(3000, lambda: [self.cadre_jeu.grid_remove(), self.afficher_ecran_titre()])

    def afficher_defaite(self):
        self.game_over = True
        self.label_defaite.grid(row=len(self.boutons)//6 + 2, column=0, columnspan=6, pady=10)
        self.root.after(3000, lambda: [self.cadre_jeu.grid_remove(), self.afficher_ecran_titre()])

    def mettre_a_jour_chrono(self):
        if self.game_over:
            return
        self.temps_restant -= 1
        self.label_timer.config(text=f"Temps restant: {self.temps_restant} secondes")
        if self.temps_restant > 0:
            self.root.after(1000, self.mettre_a_jour_chrono)
        else:
            self.afficher_defaite()

    def lancer_chrono(self):
        self.mettre_a_jour_chrono()
