# G08

import tkinter as tk
import tkinter.messagebox as box
from backend import Board, Piece, PlacementException
#importation des bibliothèques

LARG = 16    #Largeur de la grille (a remplacer par Board.width)
HAUT = 16    #Hauteur de la grille (a remplacer par Board.height)
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

		# TODO : Changer la taille en fonction de self.parent.taille
		self.board = Board(LARG, HAUT)

		### Init fenêtre
		self.scores()

		# Init plateau de jeu
		self.canvas = tk.Canvas(self, width=(PIX_L_INTERFACE+LARG*TAILLE_CARREAU), height=(PIX_H_INTERFACE+HAUT*TAILLE_CARREAU), background='white') #Board.widthm Board.height	initGrille()
		self.creation_des_pieces()
		self.initGrille()
		self.find()

		self.canvas.bind("<Button-1>", self.pointeur)
		self.canvas.grid(column=1, row=1)
		self.erreur=tk.Label(text="")
		self.erreur.grid(column=1, row=1)

		if self.parent.mode == "standard":
			# Initialisation du tableau de choix des pièces en mode standard
			def tab1(event):
				txt1=tabpieces0.create_text(200,200,text="click")
			def tab2(event):
				txt2=tabpieces1.create_text(50,50,text="click")
			def tab3(event):
				txt3=tabpieces2.create_text(50,50,text="click")
			tabpieces0 = tk.Canvas(self, background='thistle1')
			tabpieces0.grid(column=0, row = 2)
			tabpieces0.bind("<Button-1>",tab1)

			tabpieces1 = tk.Canvas(self, background='thistle2')
			tabpieces1.grid(column=1, row = 2)
			tabpieces1.bind("<Button-1>",tab2)

			tabpieces2 = tk.Canvas(self, background='thistle3')
			tabpieces2.grid(column=2, row = 2)
			tabpieces2.bind("<Button-1>",tab3)
		elif self.parent.mode == "random":
			# TODO Finir le mode aléatoire
			pass

	def scores(self):
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
		self.j2.grid(column=3, row=0)
		tk.Label(self.j2, text="joueur 2:").pack(padx=10, pady=2)
		tk.Label(self.j2, text=self.scoreJ2).pack()

	def creation_des_pieces(self):
		"""Création de toutes les pièces pouvant être jouées"""
		self.board.addPiece(Piece([
			[1, 1]
		])) # Ligne x2
		self.board.addPiece(Piece([
			[1],
			[1]
		])) # Colonne x2
		self.board.addPiece(Piece([
			[1, 1],
			[1, 1]
		])) # Carre 2x2
		self.board.addPiece(Piece([
			[0, 1],
			[1, 1],
			[1, 0]
		])) # ZigZag 2x3
		self.board.addPiece(Piece([
			[1, 1, 1]
		])) # Ligne x3
		self.board.addPiece(Piece([
			[1],
			[1],
			[1]
		])) # Colonne x3

	#====== Génération de la grille ======
	def initGrille(self):
		L = 0 #var décalage en X
		H = 0 #var décalage en Y
		for i in range(HAUT):               #Board.width
			for j in range(LARG):           #Board.height
				tag = str(j)+"-"+str(i)     #Création du tag de chaque carreau
				Pt = self.canvas.create_rectangle(PIX_L_INTERFACE/2+L,
											PIX_H_INTERFACE/2+H,
											PIX_L_INTERFACE/2+L+TAILLE_CARREAU,
											PIX_H_INTERFACE/2+H+TAILLE_CARREAU,
											tags = tag)
				L += TAILLE_CARREAU
				print(tag)
			H += TAILLE_CARREAU
			L = 0

	#====== Fonction qui change les couleurs des carreaux ======
	def find(self):
		for i in range(LARG):
			for j in range(HAUT):
				if self.board.matrix[j][i] == 1:
					tag = str(i)+"-"+str(j)
					C = self.canvas.find_withtag(tag)
					self.canvas.itemconfigure(C, fill = "green")
				if (self.board.matrix[j][i] == 2) :
					tag = str(i)+"-"+str(j)
					C = self.canvas.find_withtag(tag)
					self.canvas.itemconfigure(C, fill = "red")

	#====== Fonction qui cherche où l'on clique ======
	def pointeur(self, event):
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
			ligne = self.board.getPieceAtIndex(0)
			try:
				self.board.placePiece(ligne, Coord[1], Coord[2], color = self.cpt_tour)
			except PlacementException as e:
				# La pièce n'as pas pu être placée
				print(e.args[0])
				self.erreur.config(text=e.args[0])
				self.after(500, lambda:self.erreur.config(text=""))
				return
				# TODO Montrer le message d'erreur à l'utilisateur et annuler le placement proprement
			self.find()
			if self.cpt_tour == 1 :
				self.cpt_tour = 2
			else :
				self.cpt_tour = 1
			print(self.board.matrix)

	def reset(self):
		# TODO A finir (nettoyer le canvas)
		self.scoreJ1 = self.scoreJ2 = 0
		self.board.fillMatrix(0)


# Lancement du programme
if __name__ == "__main__":
	root = tk.Tk()
	app = FenetrePrincipale(root).pack(side="top", fill="both", expand=True)
	root.mainloop()