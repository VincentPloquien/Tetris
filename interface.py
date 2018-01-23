from functools import partial
from tkinter import *
from tkinter.messagebox import *
#importation des bibliothèques

liste=[]


	
def choix():
	liste[0].destroy()
	liste.clear()
	choix= Tk()
	liste.append(choix)
	choix.title("Taille")
	choix.resizable(width=False, height=False)
	texte= Label(choix, text='choisissez la taille de la grille de jeu:')
	texte.grid(column=0, row=0)
	button1 = Button(choix, text='taille petite', padx=10, pady=10, command=petit)
	button1.grid(column=0, row=1)
	button2 = Button(choix, text='taille moyenne', padx=10, pady=10, command=moyen)
	button2.grid(column=0, row=2)
	button3 = Button(choix, text='taille grande', padx=10, pady=10, command=grand)
	button3.grid(column=0, row=3)
	choix.mainloop()
def menu():
	liste[0].destroy()
	liste.clear()
	general()
	#TODO : retourner à l'interface de lancement
  
def petit():
	x=6
	y=6
	return(x,y)
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
	#choix()
	liste[0].destroy()
	liste.clear()

	scorej1=3
	scorej2=1

	jeu1= Tk()
	liste.append(jeu1)
	jeu1.title("Tetris")
	jeu1.resizable(width=False,height=False)
	
	debut= Label(jeu1, text="mode standard")
	debut.grid(column=1, row=0)
	j1= Frame(jeu1, borderwidth=1, relief=SUNKEN,)
	j1.grid(column=0, row=0)
	Label(j1, text="joueur 1:").pack(padx=10, pady=2)
	Label(j1, text=scorej1).pack()
	j2= Frame(jeu1, borderwidth=1, relief=SUNKEN)
	j2.grid(column=3, row=0)
	Label(j2, text="joueur 2:").pack(padx=10, pady=2)
	Label(j2, text=scorej2).pack()
	thomas= Label(jeu1, text="tableau de thomas", bg="medium aquamarine", padx=20, pady=100)
	thomas.grid(column=1, row=1)		
	menu_deroulant()

	jeu1.mainloop()
	#texte.config(text="le mode standard se lance")

def random():
	liste[0].destroy()
	liste.clear()
#	choix()
	scorej1=7
	scorej2=5

	jeu2= Tk()
	liste.append(jeu2)
	jeu2.title("Tetris")
	jeu2.resizable(width=False,height=False)
	
	debut= Label(jeu2, text="mode aléatoire")
	debut.grid(column=1, row=0)
	j1= Frame(jeu2, borderwidth=1, relief=SUNKEN,)
	j1.grid(column=0, row=0)
	Label(j1, text="joueur 1:").pack(padx=10, pady=2)
	Label(j1, text=scorej1).pack()
	j2= Frame(jeu2, borderwidth=1, relief=SUNKEN)
	j2.grid(column=3, row=0)
	Label(j2, text="joueur 2:").pack(padx=10, pady=2)
	Label(j2, text=scorej2).pack()
	thomas= Label(jeu2, text="tableau de thomas", bg="medium aquamarine", padx=20, pady=100)
	thomas.grid(column=1, row=1)		
	menu_deroulant()

	jeu2.mainloop()
	#texte.config( text="le mode aléatoire se lance")
	#TODO : lancer l'interface du mode random

def reset():
	pass

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
	
def menu_deroulant():
	menubar = Menu(liste[0])
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
	liste[0].config(menu=menubar)
	#création du menu déroulant
general()
