# G08

import tkinter as tk
import tkinter.messagebox as box
from backend import Board, Piece, PlacementException
#importation des bibliothèques

PIX_H_INTERFACE = 3   #Place pour le reste des trucs
PIX_L_INTERFACE = 3   #Place pour le reste des trucs
TAILLE_CARREAU = 25 #Coté de chaque carreau de la grille en pixel

class FenetrePrincipale(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		# Init variables
		self.mode = "standard"
		self.taille = "moyen"

		# Init menu déroulant
		self.menu_deroulant()
		
		# Init fenêtre
		self.parent.title("Tetris")
		self.parent.resizable(width=False,height=False)

		# Init jeu
		self.jeu = InterfaceJeu(self)
		self.jeu.pack()

	### Interface
	def menu_deroulant(self):
		menubar = tk.Menu(self.parent)

		menu1 = tk.Menu(menubar, tearoff=0)
		menu1.add_command(label="Nouvelle partie", command=self.reset)
		menu1.add_separator()
		menu1.add_command(label="Quitter", command=self.quitter)
		menubar.add_cascade(label="Partie", menu=menu1)

		menu2 = tk.Menu(menubar, tearoff=0)
		menu2.add_command(label="Standard", command=lambda: self.mode_de_jeu("standard"))
		menu2.add_command(label="Aléatoire (WIP)", command=lambda: self.mode_de_jeu("random"), state=tk.DISABLED)
		menubar.add_cascade(label="Mode de jeu", menu=menu2)
		
		menu3 = tk.Menu(menubar, tearoff=0)
		menu3.add_command(label="Petit", command=lambda: self.taille_du_jeu("petit"))
		menu3.add_command(label="Moyen", command=lambda: self.taille_du_jeu("moyen"))
		menu3.add_command(label="Grand", command=lambda: self.taille_du_jeu("grand"))
		menubar.add_cascade(label="Taille du jeu", menu=menu3)

		self.parent.config(menu=menubar)
	
	def quitter(self):
		if box.askyesno('Attention', 'Êtes vous sûr de vouloir fermer la fenêtre ?'):
			self.parent.destroy()
	
	### Jeu
	def mode_de_jeu(self, mode):
		if box.askyesno('Redémarrage', 'Vous vous apprêtez à recommencer une nouvelle partie en mode {}, êtes vous sûr ?'.format(mode)):
			self.mode = mode
			self.reset()
	
	def taille_du_jeu(self, taille):
		if box.askyesno('Redémarrage', 'Vous vous apprêtez à recommencer une nouvelle partie avec la taille {}, êtes vous sûr ?'.format(taille)):
			self.taille = taille
			self.reset()
	
	def reset(self):
		self.jeu.reset()

class InterfaceJeu(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		### Init variables
		self.scoreJ1 = 3
		self.scoreJ2 = 1
		self.cpt_tour = 1
		self.largeur = 6
		self.piece_choisie = None
		self.listePieces = []
		self.board = None

		### Init interface
		self.initInterface()

		# Init plateau de jeu
		self.initBoard()
		self.initGrille()
		self.find()

		# Gestion du mode de jeu
		if self.parent.mode == "standard":
			# Initialisation du tableau de choix des pièces en mode standard
			def tab1(_):
				self.piece_choisie=self.listePieces[0]
			def tab2(_):
				self.piece_choisie=self.listePieces[1]
			def tab3(_):
				self.piece_choisie=self.listePieces[2]
				
			self.tabpieces0 = tk.Canvas(self, width=(100), height=(100), background='thistle1')
			self.tabpieces0.grid(column=0, row = 3)
			self.tabpieces0.bind("<Button-1>",tab1)

			self.tabpieces1 = tk.Canvas(self,width=(100), height=(100), background='thistle2')
			self.tabpieces1.grid(column=1, row = 3)
			self.tabpieces1.bind("<Button-1>",tab2)

			self.tabpieces2 = tk.Canvas(self,width=(100), height=(100), background='thistle3')
			self.tabpieces2.grid(column=2, row = 3)
			self.tabpieces2.bind("<Button-1>",tab3)

			self.initChoix()
		elif self.parent.mode == "random":
			# TODO Finir le mode aléatoire
			pass

	def initInterface(self):
		# Label mode de jeu
		self.modeLabel = tk.Label(self, text="Mode {}".format(self.parent.mode))
		self.modeLabel.grid(column=1, row=0)

		# Label score J1
		self.j1 = tk.Frame(self, borderwidth=1, relief=tk.SUNKEN)
		self.j1.grid(column=0, row=0)
		tk.Label(self.j1, text="Joueur 1").pack(padx=10, pady=2)
		tk.Label(self.j1, text=self.scoreJ1).pack()
		
		# Label score J2
		self.j2= tk.Frame(self, borderwidth=1, relief=tk.SUNKEN)
		self.j2.grid(column=2, row=0)
		tk.Label(self.j2, text="joueur 2:").pack(padx=10, pady=2)
		tk.Label(self.j2, text=self.scoreJ2).pack()

		# Label message d'erreur
		self.erreur = tk.Label(self, text="")
		self.erreur.grid(column=1, row=1)

		self.canvas = tk.Canvas(self, background='white')
		self.canvas.bind("<Button-1>", self.pointeur)
		self.canvas.grid(column=1, row=2)

	def initBoard(self):
		"""Initialisation du backend & Création de toutes les pièces pouvant être jouées"""
		# Gestion de la taille du plateau
		if self.parent.taille == "petit":
			self.largeur = 6
		elif self.parent.taille == "moyen":
			self.largeur = 10
		elif self.parent.taille == "grand":
			self.largeur = 14

		# Init du Board et Canvas
		self.board = Board(self.largeur, self.largeur)
		self.canvas.config(width=(PIX_L_INTERFACE+self.largeur*TAILLE_CARREAU), height=(PIX_H_INTERFACE+self.largeur*TAILLE_CARREAU))
		print(self.largeur)

		self.board.addPiece(Piece([
			[1, 1],
			[1, 1]
		])) # Carre

		self.board.addPiece(Piece([
			[1, 0],
			[1, 1],
			[0, 1]
		])) # ZigZag vertical
		self.board.addPiece(Piece([
			[1, 1, 0],
			[0, 1, 1]
		])) # ZigZag horizontal

		self.board.addPiece(Piece([
			[1, 0],
			[1, 0],
			[1, 1]
		])) # L vertical
		self.board.addPiece(Piece([
			[1, 1],
			[0, 1],
			[0, 1]
		])) # L vertical

		self.board.addPiece(Piece([
			[1, 1, 1],
			[0, 0, 1]
		])) # L horizontal
		self.board.addPiece(Piece([
			[1, 0, 0],
			[1, 1, 1]
		])) # L horizontal

		self.board.addPiece(Piece([
			[1, 0],
			[1, 1],
			[1, 0]
		])) # Triangle vertical
		self.board.addPiece(Piece([
			[1, 1, 1],
			[0, 1, 0]
		])) # Triangle horizontal

		self.board.addPiece(Piece([
			[1, 1, 1]
		])) # Ligne
		self.board.addPiece(Piece([
			[1],
			[1],
			[1]
		])) # Colonne

	def initChoix(self):
		cpt = 0
		L = 0 #var décalage en X
		H = 0 #var décalage en Y
		while cpt < 3:
			if cpt == 0 :
				self.listePieces.append(self.board.getRandomPiece())
				cpt =1
			else :
				pt = self.board.getRandomPiece()
				if pt not in self.listePieces:
					self.listePieces.append(pt)
					cpt += 1

		S1 = self.listePieces[0].shape

		for y in range(len(S1)):
			for x in range(0, len(S1[y])):
				if S1[y][x] == 1 :
					self.tabpieces0.create_rectangle(20+L,
												20+H,
												20+L+TAILLE_CARREAU,
												20+H+TAILLE_CARREAU,
												fill = 'blue')
				L += TAILLE_CARREAU
			H += TAILLE_CARREAU
			L = 0
		self.tabpieces2.grid(column=0, row = 3)
		L = 0 #var décalage en X
		H = 0 #var décalage en Y

		S1 = self.listePieces[1].shape
		for y in range(len(S1)):
			for x in range(0, len(S1[y])):
				if S1[y][x] == 1 :
					self.tabpieces1.create_rectangle(20+L,
												20+H,
												20+L+TAILLE_CARREAU,
												20+H+TAILLE_CARREAU,
												fill = 'blue')
				L += TAILLE_CARREAU
			H += TAILLE_CARREAU
			L = 0
		self.tabpieces2.grid(column=1, row = 3)

		L = 0 #var décalage en X
		H = 0 #var décalage en Y

		S1 = self.listePieces[2].shape
		for y in range(len(S1)):
			for x in range(0, len(S1[y])):
				if S1[y][x] == 1 :
					self.tabpieces2.create_rectangle(20+L,
												20+H,
												20+L+TAILLE_CARREAU,
												20+H+TAILLE_CARREAU,
												fill = 'blue')
				L += TAILLE_CARREAU
			H += TAILLE_CARREAU
			L = 0
		self.tabpieces2.grid(column=2, row = 3)

	def initGrille(self):
		"""Génération de la grille"""
		L = 0 #var décalage en X
		H = 0 #var décalage en Y
		for i, ligne in enumerate(self.board.matrix):
			for j, pixel in enumerate(ligne):
				tag = str(j)+"-"+str(i)     #Création du tag de chaque carreau
				self.canvas.create_rectangle(PIX_L_INTERFACE/2+L,
											PIX_H_INTERFACE/2+H,
											PIX_L_INTERFACE/2+L+TAILLE_CARREAU,
											PIX_H_INTERFACE/2+H+TAILLE_CARREAU,
											tags = tag)
				L += TAILLE_CARREAU
				# print(tag)
			H += TAILLE_CARREAU
			L = 0

	def find(self):
		"""Fonction qui change les couleurs des carreaux"""
		for i, ligne in enumerate(self.board.matrix):
			for j, pixel in enumerate(ligne):
				tag = str(j)+"-"+str(i)
				C = self.canvas.find_withtag(tag)
				if pixel == 1:
					self.canvas.itemconfigure(C, fill = "green")
				if pixel == 2:
					self.canvas.itemconfigure(C, fill = "red")

	def pointeur(self, event):
		"""Fonction qui cherche où l'on clique"""
		Coord = ["IsValid", "X", "Y"]
		if (event.x > PIX_L_INTERFACE/2 and event.x < PIX_L_INTERFACE/2+self.largeur*TAILLE_CARREAU):
			X_Carreau = int(abs((event.x - PIX_L_INTERFACE/2))//TAILLE_CARREAU)
			Coord[0] = "Valid"
			Coord[1] = X_Carreau
			# print(X_Carreau)
		else :
			Coord[0] = "Not_Valid"

		if (event.y > PIX_H_INTERFACE/2 and event.y < PIX_H_INTERFACE/2+self.largeur*TAILLE_CARREAU and Coord[0] == "Valid"):
			Y_Carreau = int(abs((((PIX_H_INTERFACE+self.largeur*TAILLE_CARREAU-event.y) - PIX_H_INTERFACE/2)//TAILLE_CARREAU)-(self.largeur-1)))
			Coord[2] = Y_Carreau
			# print(Y_Carreau)
		else :
			Coord[0] = "Not_Valid"
		
		if (Coord[0] == "Valid"):
			try:
				self.board.placePiece(self.piece_choisie, Coord[1], Coord[2], color = self.cpt_tour)
			except PlacementException as e:
				# La pièce n'as pas pu être placée
				# print(e.args[0])
				self.erreur.config(text=e.args[0])
				self.after(1000, lambda:self.erreur.config(text=""))
				return
				# TODO Montrer le message d'erreur à l'utilisateur et annuler le placement proprement
			self.find()
			if self.cpt_tour == 1 :
				self.cpt_tour = 2
			else :
				self.cpt_tour = 1
			# print(self.board.matrix)

	def reset(self):
		"""Replace tout le jeu à son état initial et relance une partie"""
		# Reset des variables
		self.scoreJ1 = self.scoreJ2 = 0
		self.piece_choisie = None
		self.listePieces = []
		
		# Reset des canvas
		self.canvas.delete("all")
		self.tabpieces0.delete("all")
		self.tabpieces1.delete("all")
		self.tabpieces2.delete("all")

		# Re-init
		self.initBoard()
		self.initGrille()
		self.initChoix()


# Lancement du programme
if __name__ == "__main__":
	root = tk.Tk()
	app = FenetrePrincipale(root).pack(side="top", fill="both", expand=True)
	root.mainloop()