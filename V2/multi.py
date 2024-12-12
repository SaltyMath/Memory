import tkinter as tk
from tkinter import simpledialog, messagebox
import random

class Multijoueur:
    def __init__(self, root, nb_joueurs, noms_joueurs, ecran_titre, afficher_ecran_titre):
        self.root = root
        self.nb_joueurs = nb_joueurs
        self.noms_joueurs = noms_joueurs
        self.nb_cartes = 24  # 24 paires de cartes pour un total de 48 cartes
        self.ecran_titre = ecran_titre
        self.afficher_ecran_titre = afficher_ecran_titre
        self.game_over = False
        self.boutons = []
        self.cartes_revelees = []
        self.par_pair = [False] * (self.nb_cartes * 2)
        self.cartes = list(range(self.nb_cartes)) * 2
        random.shuffle(self.cartes)
        self.joueurs = [{"nom": nom, "score": 0} for nom in noms_joueurs]
        self.index_joueur_actuel = 0

        # Calculer la taille de la fenêtre pour une grille de 8x6
        self.largeur_fenetre = 13 * 50  # 8 colonnes de 100 pixels
        self.hauteur_fenetre = 8 * 100  # 6 lignes de 100 pixels + 1 ligne pour l'image de victoire
        self.root.geometry(f"{self.largeur_fenetre}x{self.hauteur_fenetre}")

        self.cadre_jeu = tk.Frame(root)
        
        self.label_scores = tk.Label(self.cadre_jeu, text="", font=("Helvetica", 16))
        self.label_scores.grid(row=0, column=0, columnspan=8)
        
        self.label_joueur_actuel = tk.Label(self.cadre_jeu, text="", font=("Helvetica", 16))
        self.label_joueur_actuel.grid(row=1, column=0, columnspan=8)
        
        for i in range(self.nb_cartes * 2):
            bouton = tk.Button(self.cadre_jeu, text='', width=10, height=5, command=lambda i=i: self.on_bouton_click(i))
            bouton.grid(row=(i // 8) + 2, column=i % 8)  # Placer les boutons en 8 colonnes
            self.boutons.append(bouton)
        
        self.image_victoire = tk.PhotoImage(file="./Memory/V2/ImgMp4/victory.png")
        self.label_victoire = tk.Label(self.cadre_jeu, image=self.image_victoire)
        
        self.image_defaite = tk.PhotoImage(file="./Memory/V2/ImgMp4/defeat.png")
        self.label_defaite = tk.Label(self.cadre_jeu, image=self.image_defaite)
        
        self.afficher_scores()
        self.label_joueur_actuel.config(text=f"Tour de: {self.joueurs[self.index_joueur_actuel]['nom']}")
        self.cadre_jeu.grid(row=0, column=0, sticky="nsew")

    def reinitialiser_scores(self):
        for joueur in self.joueurs:
            joueur['score'] = 0
        self.index_joueur_actuel = 0

    def afficher_scores(self):
        scores = "Scores:\n"
        for joueur in self.joueurs:
            scores += f"{joueur['nom']}: {joueur['score']}\n"
        self.label_scores.config(text=scores)

    def changer_joueur(self):
        if len(self.joueurs) == 0:
            messagebox.showerror("Erreur", "Aucun joueur disponible pour changer!")
            return

        self.index_joueur_actuel = (self.index_joueur_actuel + 1) % len(self.joueurs)
        self.label_joueur_actuel.config(text=f"Tour de: {self.joueurs[self.index_joueur_actuel]['nom']}")

    def incrementer_score_joueur_actuel(self):
        if len(self.joueurs) > 0:
            self.joueurs[self.index_joueur_actuel]['score'] += 1

    def get_joueur_actuel_nom(self):
        if len(self.joueurs) > 0:
            return self.joueurs[self.index_joueur_actuel]['nom']
        return "Aucun joueur"

    def get_gagnant(self):
        if len(self.joueurs) > 0:
            return max(self.joueurs, key=lambda joueur: joueur['score'])
        return None

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
            self.incrementer_score_joueur_actuel()
            self.afficher_scores()
        else:
            for i in self.cartes_revelees:
                self.boutons[i].config(text='', state='normal')
            self.changer_joueur()
        self.cartes_revelees = []

        if all(self.par_pair):
            self.game_over = True
            self.afficher_victoire()

    def afficher_victoire(self):
        self.label_victoire.grid(row=len(self.boutons)//8 + 3, column=0, columnspan=8, pady=10)
        gagnant = self.get_gagnant()
        messagebox.showinfo("Victoire", f"Le gagnant est {gagnant['nom']} avec un score de {gagnant['score']} !")
        self.root.after(3000, lambda: [self.cadre_jeu.grid_remove(), self.afficher_ecran_titre()])

    def afficher_defaite(self):
        self.game_over = True
        self.label_defaite.grid(row=len(self.boutons)//8 + 3, column=0, columnspan=8, pady=10)
        self.root.after(3000, lambda: [self.cadre_jeu.grid_remove(), self.afficher_ecran_titre()])
