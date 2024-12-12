import tkinter as tk
from tkinter import messagebox
import random

# Configuration de la fenêtre principale
root = tk.Tk()
root.title("Memory Game")

# Création de la grille de cartes
cards = list(range(8)) * 2
random.shuffle(cards)
buttons = []
revealed_cards = []
matched = [False] * 16

def on_button_click(index):
    global revealed_cards
    if len(revealed_cards) == 2 or matched[index]:
        return

    buttons[index].config(text=cards[index], state='disabled')
    revealed_cards.append(index)

    if len(revealed_cards) == 2:
        root.after(1000, check_match)

def check_match():
    global revealed_cards
    if cards[revealed_cards[0]] == cards[revealed_cards[1]]:
        matched[revealed_cards[0]] = True
        matched[revealed_cards[1]] = True
    else:
        for i in revealed_cards:
            buttons[i].config(text='', state='normal')
    revealed_cards = []

# Création des boutons
for i in range(16):
    button = tk.Button(root, text='', width=10, height=3, command=lambda i=i: on_button_click(i))
    button.grid(row=i//4, column=i%4)
    buttons.append(button)

# Lancement de la boucle principale
root.mainloop()