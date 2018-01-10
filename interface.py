from functools import partial
from tkinter import *
from tkinter.messagebox import *
#importation des bibliothèques

liste=[]

def reset():
	pass
	#texte.config( text="la partie recommence avec les mêmes paramètres")

def menu():
	liste[0].destroy()
	liste.clear()
	general()
	#TODO : retourner à l'interface de lancement

def petit():
	if askyesno('redémarrage', 'vous vous apprêtez à recommencer une nouvelle partie avec la taille petite, êtes vous sur?'):
	 pass
	#texte.config( text="la partie redémarre avec la taille choisie : petite")
def moyen():
	if askyesno('redémarrage', 'vous vous apprêtez à recommencer une nouvelle partie avec la taille moyenne, êtes vous sur?'):
	 pass
	#texte.config( text="la partie redémarre avec la taille choisie : moyenne")

def grand():
	if askyesno('redémarrage', 'vous vous apprêtez à recommencer une nouvelle partie avec la taille grande, êtes vous sur?'):
	 pass
	#texte.config( text="la partie redémarre avec la taille choisie : grande")

def quitter():
	if askyesno('attention', 'êtes vous sur de vouloir fermer la fenêtre?'):
	 liste[0].destroy()
	 liste.clear()

def standard():
	liste[0].destroy()
	liste.clear()

	scorej1=3
	scorej2=1

	jeu= Tk()
	liste.append(jeu)
	jeu.title("Tetris")
	jeu.resizable(width=False,height=False)
	
	debut= Label(jeu, text="mode standard")
	debut.grid(column=1, row=0)
	j1= Frame(jeu, borderwidth=1, relief=SUNKEN,)
	j1.grid(column=0, row=0)
	Label(j1, text="joueur 1:").pack(padx=10, pady=2)
	Label(j1, text=scorej1).pack()
	j2= Frame(jeu, borderwidth=1, relief=SUNKEN)
	j2.grid(column=3, row=0)
	Label(j2, text="joueur 2:").pack(padx=10, pady=2)
	Label(j2, text=scorej2).pack()
	thomas= Label(jeu, text="tableau de thomas", bg="medium aquamarine", padx=20, pady=100)
	thomas.grid(column=1, row=1)

	menubar = Menu(jeu)
	menu1 = Menu(menubar, tearoff=0)
	menu1.add_command(label="Lancer une nouvelle partie", command=reset)
	menu1.add_command(label="retour au choix du mode de jeu", command=menu)
	menu1.add_separator()
	menu1.add_command(label="Quitter", command=quitter)
	menubar.add_cascade(label="Menu", menu=menu1)
	menu2 = Menu(menubar, tearoff=0)
	menu2.add_command(label="Petit", command=petit)
	menu2.add_command(label="Moyen", command=moyen)
	menu2.add_command(label="Grand", command=grand)
	menubar.add_cascade(label="Taille du jeu", menu=menu2)
	jeu.config(menu=menubar)
	#création du menu déroulant		

	jeu.mainloop()
	#texte.config(text="le mode standard se lance")

def random():
	pass
	#texte.config( text="le mode aléatoire se lance")
	#TODO : lancer l'interface du mode random

def general():
	fenetre = Tk()
	fenetre.title("Menu principal")
	#création et nommage de la fenêtre de jeu

	button1 = Button(fenetre, text='mode standard', padx=10, pady=10, command=standard)
	button1.grid(column=0, row=2)
	button2 = Button(fenetre, text='mode aléatoire', padx=10, pady=10, command=random)
	button2.grid(column=0, row=3)
	#création des boutons du menu principal

	texte = Label(fenetre, text="            Bienvenue \n choisissez votre mode de jeu",
	padx="100", pady="10")
	texte.grid(columnspan=1, row=1)
	#affichage du texte temporaire explicatif
	
	liste.append(fenetre)
	fenetre.mainloop()
	print("ok")
general()
