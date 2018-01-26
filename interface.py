from functools import partial
from tkinter import *
from tkinter.messagebox import *
from backend import Board, Piece, PlacementException
#importation des bibliothèques

liste=[]
LARG = 16    #Largeur de la grille (a remplacer par Board.width)
HAUT = 16    #Hauteur de la grille (a remplacer par Board.height)
board = Board(LARG, HAUT)
PIX_H_INTERFACE = 3   #Place pour le reste des trucs
PIX_L_INTERFACE = 3   #Place pour le reste des trucs
TAILLE_CARREAU = 25 #Coté de chaque carreau de la grille en pixel
global cpt_tour
cpt_tour = 1

def initPieces():
	board.addPiece(Piece([
		[1, 1]
	]))
	board.addPiece(Piece([
		[1],
		[1]
	]))
	board.addPiece(Piece([
		[1, 1],
		[1, 1]
	]))
	board.addPiece(Piece([
		[0, 1],
		[1, 1],
		[1, 0]
	]))
	board.addPiece(Piece([
		[1, 1, 1]
	]))
	board.addPiece(Piece([
		[1],
		[1],
		[1]
	]))

#====== Génération de la grille ======
def initGrille():
	global canvas
	L = 0 #var décalage en X
	H = 0 #var décalage en Y
	for i in range(HAUT):               #Board.width
		for j in range(LARG):           #Board.height
			tag = str(j)+"-"+str(i)     #Création du tag de chaque carreau
			Pt = canvas.create_rectangle(PIX_L_INTERFACE/2+L,
										 PIX_H_INTERFACE/2+H,
										 PIX_L_INTERFACE/2+L+TAILLE_CARREAU,
										 PIX_H_INTERFACE/2+H+TAILLE_CARREAU,
										 tags = tag)
			L += TAILLE_CARREAU
			print(tag)
		H += TAILLE_CARREAU
		L = 0

#====== Fonction qui change les couleurs des carreaux ======
def find():
	global canvas
	for i in range(LARG):
		for j in range(HAUT):
			if board.matrix[j][i] == 1:
				tag = str(i)+"-"+str(j)
				C = canvas.find_withtag(tag)
				canvas.itemconfigure(C, fill = "green")
			if (board.matrix[j][i] == 2) :
				tag = str(i)+"-"+str(j)
				C = canvas.find_withtag(tag)
				canvas.itemconfigure(C, fill = "red")
				
#====== Fonciton qui cherche où l'on clique ======
def pointeur(event):
	global canvas
	global cpt_tour
	#global type de pièce
	Coord = ["IsValid", "X", "Y"]
	if (event.x > PIX_L_INTERFACE/2 and event.x < PIX_L_INTERFACE/2+LARG*TAILLE_CARREAU):
		X_Carreau = int(abs((event.x - PIX_L_INTERFACE/2))//TAILLE_CARREAU)
		Coord[0] = "Valid"
		Coord[1] = X_Carreau
		print(X_Carreau)
	else :
		Coord[0] = "Not_Valid"

	if (event.y > PIX_H_INTERFACE/2 and event.y < PIX_H_INTERFACE/2+HAUT*TAILLE_CARREAU and Coord[0] == "Valid"):
		Y_Carreau = int(abs((((PIX_H_INTERFACE+HAUT*TAILLE_CARREAU-event.y) - PIX_H_INTERFACE/2)//TAILLE_CARREAU)-(HAUT-1)))
		Coord[2] = Y_Carreau
		print(Y_Carreau)
	else :
		Coord[0] = "Not_Valid"
	
	if (Coord[0] == "Valid"):
		ligne = board.getPieceAtIndex(0)
		try:
			board.placePiece(ligne, Coord[1], Coord[2], color = cpt_tour)
		except PlacementException as e:
			# La pièce n'as pas pu être placée
			print(e.args[0])
			# TODO Montrer le message d'erreur à l'utilisateur et annuler le placement proprement
		find()
		if cpt_tour == 1 :
			cpt_tour = 2
		else :
			cpt_tour = 1
		print(board.matrix)



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
	j1= Frame(jeu1, borderwidth=1, relief=SUNKEN)
	j1.grid(column=0, row=0)
	Label(j1, text="joueur 1:").pack(padx=10, pady=2)
	Label(j1, text=scorej1).pack()
	j2= Frame(jeu1, borderwidth=1, relief=SUNKEN)
	j2.grid(column=3, row=0)
	Label(j2, text="joueur 2:").pack(padx=10, pady=2)
	Label(j2, text=scorej2).pack()

	#========> Thomas
	global canvas
	initPieces()
	canvas = Canvas(jeu1, width=(PIX_L_INTERFACE+LARG*TAILLE_CARREAU), height=(PIX_H_INTERFACE+HAUT*TAILLE_CARREAU), background='white') #Board.widthm Board.height	initGrille()
	initGrille()
	find()
	canvas.bind("<Button-1>", pointeur)
	canvas.grid(column=1, row=1)
	#========>

	menu_deroulant()
	tabpieces0 = Canvas(jeu1, background='thistle1')
	tabpieces0.grid(column=0, row = 2)
	tabpieces1 = Canvas(jeu1, background='thistle2')
	tabpieces1.grid(column=1, row = 2)
	tabpieces2 = Canvas(jeu1, background='thistle3')
	tabpieces2.grid(column=2, row = 2)
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
	canvas= Label(jeu2, text="board.matrix de thomas", bg="medium aquamarine", padx=20, pady=100)
	canvas.grid(column=1, row=1)		
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
