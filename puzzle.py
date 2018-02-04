# G08
# PITHON Mathieu
# PLOQUIEN Vincent
# PREVOST Thomas

#importation des bibliothèques
import tkinter as tk
import tkinter.messagebox as box
import pprint
from backend import Board, Piece, PlacementException

# Constantes pour la marge et la taille d'un carreau
PIX_H_INTERFACE = 3
PIX_L_INTERFACE = 3
TAILLE_CARREAU = 25

class FenetrePrincipale(tk.Frame):
	"""Objet Tkinter contenant toute l'application"""
	def __init__(self, parent, *args, **kwargs):
		"""Initialisation de la fenêtre"""

		# Init de l'objet Tkinter
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		# Init fenêtre
		self.parent.title("Tetris")
		self.parent.resizable(width=False,height=False)

		# Init variables
		self.mode = "standard"
		self.taille = "moyen"
		self.DEBUG = False

		# Init menu déroulant
		self.menu_deroulant()
		
		# Init jeu
		self.jeu = InterfaceJeu(self)
		self.jeu.pack()

	### Interface
	def menu_deroulant(self):
		"""Créer un menu déroulant pour modifier les paramètres de la partie"""
		menubar = tk.Menu(self.parent)

		# Menu "Partie"
		menu1 = tk.Menu(menubar, tearoff=0)
		menu1.add_command(label="Nouvelle partie", command=self.reset)
		menu1.add_checkbutton(label="Mode débug", command=self.debug)
		menu1.add_separator()
		menu1.add_command(label="Quitter", command=self.quitter)
		menubar.add_cascade(label="Partie", menu=menu1)

		# Menu "Mode de jeu"
		menu2 = tk.Menu(menubar, tearoff=0)
		menu2.add_command(
			label="Standard",
			command=lambda: self.mode_de_jeu("standard"))
		menu2.add_command(
			label="Aléatoire (WIP)",
			command=lambda: self.mode_de_jeu("random"), state=tk.DISABLED)
		menubar.add_cascade(label="Mode de jeu", menu=menu2)
		
		# Menu "Taille de jeu"
		menu3 = tk.Menu(menubar, tearoff=0)
		menu3.add_command(
			label="Petit",
			command=lambda: self.taille_du_jeu("petit"))
		menu3.add_command(
			label="Moyen",
			command=lambda: self.taille_du_jeu("moyen"))
		menu3.add_command(
			label="Grand",
			command=lambda: self.taille_du_jeu("grand"))
		menubar.add_cascade(label="Taille du jeu", menu=menu3)

		# Ajout du menu
		self.parent.config(menu=menubar)
	
	def debug(self):
		"""Gère le sous-menu de débug"""
		self.DEBUG = not self.DEBUG

	def quitter(self):
		"""Gère le menu pour quitter le jeu"""
		if box.askyesno('Attention', 'Êtes vous sûr de vouloir fermer la fenêtre ?'):
			self.parent.destroy()
	
	### Jeu
	def mode_de_jeu(self, mode):
		"""Gère le menu pour changer le mode de jeu en *mode*"""
		if box.askyesno(
			'Redémarrage',
			'Voulez vous vraiment recommencer une nouvelle partie en mode {} ?'.format(mode)):
			self.mode = mode
			self.reset()
	
	def taille_du_jeu(self, taille):
		"""Gère le menu pour changer la taille du jeu à *taille*"""
		if box.askyesno(
			'Redémarrage',
			'Voulez vous vraiment recommencer une nouvelle partie avec la taille {} ?'.format(taille)):
			self.taille = taille
			self.reset()

	def reset(self):
		"""Demande le reset de la partie"""
		self.jeu.reset()

class InterfaceJeu(tk.Frame):
	"""Objet Tkinter contenant tout le jeu"""
	def __init__(self, parent, *args, **kwargs):
		"""Initialisation du jeu"""
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		# Init variables
		self.scoreJ1 = self.scoreJ2 = 0
		self.cpt_tour = 1
		self.largeur = 6
		self.piece_choisie = None
		self.board = None
		self.listePieces = []

		# Init interface
		self.initInterface()

		# Init plateau de jeu
		self.initBoard()
		self.initGrille()
		self.updateColors()

		# Gestion du mode de jeu
		if self.parent.mode == "standard":
			# Initialisation du tableau de choix des pièces en mode standard
			def abandon():
				
				# Mise à jour des scores
				if self.cpt_tour == 1:
					tk.messagebox.showinfo(
						"Victoire !",
						"Bravo ! Le joueur 2 à remporté la partie par abandon.")
					self.scoreJ2 += 1
				else:
					tk.messagebox.showinfo(
						"Victoire !",
						"Bravo ! Le joueur 1 à remporté la partie par abandon.")
					self.scoreJ1 += 1
			
				self.scj1.config(text=self.scoreJ1)
				self.scj2.config(text=self.scoreJ2)

				# Verrouillage du jeu
				self.abandonner.config(state=tk.DISABLED)
				self.canvas.unbind("<Button-1>")
				
			def tab1(_):
				self.piece_choisie=self.listePieces[0]
			def tab2(_):
				self.piece_choisie=self.listePieces[1]
			def tab3(_):
				self.piece_choisie=self.listePieces[2]
			
			self.abandonner=tk.Button(self, text="J'abandonne", command=abandon)
			self.abandonner.grid(column=2, row=2)
			# Création de chaque canvas contenant les pièces à jouer	
			self.tabpieces0 = tk.Canvas(self,
				width=(100), height=(100),
				background='thistle2')
			self.tabpieces0.grid(column=0, row = 3)
			self.tabpieces0.bind("<Button-1>",tab1)

			self.tabpieces1 = tk.Canvas(self,
				width=(100), height=(100),
				background='thistle2')
			self.tabpieces1.grid(column=1, row = 3)
			self.tabpieces1.bind("<Button-1>",tab2)

			self.tabpieces2 = tk.Canvas(self,
				width=(100), height=(100),
				background='thistle2')
			self.tabpieces2.grid(column=2, row = 3)
			self.tabpieces2.bind("<Button-1>",tab3)

			self.initChoix()
		elif self.parent.mode == "random":
			# TODO Finir le mode aléatoire
			pass

	def initInterface(self):
		"""Initialisation des composants Tkinter pour le jeu"""

		# Label "mode de jeu"
		self.modeLabel = tk.Label(self, text="Mode {}".format(self.parent.mode))
		self.modeLabel.grid(column=1, row=0)

		# Label "score J1"
		self.j1 = tk.Frame(self, borderwidth=1, relief=tk.SUNKEN)
		self.j1.grid(column=0, row=0)
		tk.Label(self.j1, text="Joueur 1").pack(padx=10, pady=2)
		self.scj1 = tk.Label(self.j1, text=self.scoreJ1)
		self.scj1.pack()
		
		# Label "score J2"
		self.j2= tk.Frame(self, borderwidth=1, relief=tk.SUNKEN)
		self.j2.grid(column=2, row=0)
		tk.Label(self.j2, text="Joueur 2:").pack(padx=10, pady=2)
		self.scj2 = tk.Label(self.j2, text=self.scoreJ2)
		self.scj2.pack()

		# Label message d'erreur
		self.erreur = tk.Label(self, text="")
		self.erreur.grid(column=1, row=1)

		# Canvas du jeu
		self.canvas = tk.Canvas(self, background='white')
		self.canvas.bind("<Button-1>", self.pointeur)
		self.canvas.grid(column=1, row=2)

	def initBoard(self):
		"""Initialisation du backend & Création de toutes les pièces jouables"""

		# Gestion de la taille du plateau
		if self.parent.taille == "petit":
			self.largeur = 6
		elif self.parent.taille == "moyen":
			self.largeur = 10
		elif self.parent.taille == "grand":
			self.largeur = 14

		# Init du Board et Canvas
		self.board = Board(self.largeur, self.largeur)
		self.canvas.config(
			width=(PIX_L_INTERFACE+self.largeur*TAILLE_CARREAU),
			height=(PIX_H_INTERFACE+self.largeur*TAILLE_CARREAU))
		if self.parent.DEBUG:
			print("Largeur du plateau: ", self.largeur)

		# Ajout des différentes pièces dans la librairie
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
	def centrage(self,x,y):
		ctr=[]
		if y == 1 :
			ctr.append(50 - (TAILLE_CARREAU+1)/2)
		elif y == 2 :
			ctr.append(50 - TAILLE_CARREAU)
		elif y == 3 :
			ctr.append(50 - (TAILLE_CARREAU+(TAILLE_CARREAU+1)/2))
			
		if x == 1 :
			ctr.append(50 - (TAILLE_CARREAU+1)/2)
		elif x == 2 :
			ctr.append(50 - TAILLE_CARREAU)
		elif x == 3 :
			ctr.append(50 - (TAILLE_CARREAU+(TAILLE_CARREAU+1)/2))
		
		return(ctr)

	def initChoix(self):
		"""Initialisation du canvas de choix des pièces"""
		
		# Création d'une liste de 3 pièces à jouer uniques et aléatoires
		plc = []
		cpt = 0
		while cpt < 3:
			if cpt == 0 :
				# Ajoute une première pièce
				self.listePieces.append(self.board.getRandomPiece())
				cpt =1
			else :
				# Ajoute le reste des pièces en vérifiant si elles sont bien uniques
				pt = self.board.getRandomPiece()
				if pt not in self.listePieces:
					self.listePieces.append(pt)
					cpt += 1

		# Dessine la forme de la pièce n°1
		L = H = 0
		piece = self.listePieces[0].shape
		for ligne in piece:
			for pixel in ligne:
				if pixel == 1 :
					plc = self.centrage(len(piece),len(piece[0]))
					self.tabpieces0.create_rectangle(plc[0]+L,
												plc[1]+H,
												plc[0]+L+TAILLE_CARREAU,
												plc[1]+H+TAILLE_CARREAU,
												fill = 'blue')
				L += TAILLE_CARREAU
			H += TAILLE_CARREAU
			L = 0
		self.tabpieces2.grid(column=0, row = 3)
		
		# Dessine la forme de la pièce n°2
		L = H = 0
		piece = self.listePieces[1].shape
		for ligne in piece:
			for pixel in ligne:
				if pixel == 1 :
					plc = self.centrage(len(piece),len(piece[0]))
					self.tabpieces1.create_rectangle(plc[0]+L,
												plc[1]+H,
												plc[0]+L+TAILLE_CARREAU,
												plc[1]+H+TAILLE_CARREAU,
												fill = 'blue')
				L += TAILLE_CARREAU
			H += TAILLE_CARREAU
			L = 0
		self.tabpieces2.grid(column=1, row = 3)

		# Dessine la forme de la pièce n°3
		L = H = 0
		piece = self.listePieces[2].shape
		for ligne in piece:
			for pixel in ligne:
				if pixel == 1 :
					plc = self.centrage(len(piece),len(piece[0]))
					self.tabpieces2.create_rectangle(plc[0]+L,
												plc[1]+H,
												plc[0]+L+TAILLE_CARREAU,
												plc[1]+H+TAILLE_CARREAU,
												fill = 'blue')
				L += TAILLE_CARREAU
			H += TAILLE_CARREAU
			L = 0
		self.tabpieces2.grid(column=2, row = 3)

	def initGrille(self):
		"""Initialisation de la grille"""
		L = H = 0
		for i, ligne in enumerate(self.board.matrix):
			for j, _ in enumerate(ligne):
				tag = str(j)+"-"+str(i)     #Création du tag de chaque carreau
				self.canvas.create_rectangle(PIX_L_INTERFACE/2+L,
											PIX_H_INTERFACE/2+H,
											PIX_L_INTERFACE/2+L+TAILLE_CARREAU,
											PIX_H_INTERFACE/2+H+TAILLE_CARREAU,
											tags = tag)
				L += TAILLE_CARREAU
				if self.parent.DEBUG:
					print("Tag : {}".format(tag))
			H += TAILLE_CARREAU
			L = 0

	def updateColors(self):
		"""Met à jour les couleurs des carreaux"""
		for i, ligne in enumerate(self.board.matrix):
			for j, pixel in enumerate(ligne):
				tag = str(j)+"-"+str(i)
				C = self.canvas.find_withtag(tag)
				if pixel == 1:
					self.canvas.itemconfigure(C, fill = "green")
				if pixel == 2:
					self.canvas.itemconfigure(C, fill = "red")

	def pointeur(self, event):
		"""Gère le clic sur un carreau et le placement de la pièce"""
		Coord = ["IsValid", "X", "Y"]

		# Vérifie la position de la souris en X
		if (event.x > PIX_L_INTERFACE/2
		and event.x < PIX_L_INTERFACE/2+self.largeur*TAILLE_CARREAU):
			X_Carreau = int(abs((event.x - PIX_L_INTERFACE/2))//TAILLE_CARREAU)
			Coord[0] = "Valid"
			Coord[1] = X_Carreau
			if self.parent.DEBUG:
				print("Carreau en X: {}".format(X_Carreau))
		else :
			Coord[0] = "Not_Valid"

		# Vérifie la position de la souris en Y
		if (event.y > PIX_H_INTERFACE/2
		and event.y < PIX_H_INTERFACE/2+self.largeur*TAILLE_CARREAU
		and Coord[0] == "Valid"):
			Y_Carreau = int(abs(
				(((PIX_H_INTERFACE+self.largeur*TAILLE_CARREAU-event.y)
				- PIX_H_INTERFACE/2)//TAILLE_CARREAU)-(self.largeur-1)
			))
			Coord[2] = Y_Carreau
			if self.parent.DEBUG:
				print("Carreau en Y: {}".format(Y_Carreau))
		else :
			Coord[0] = "Not_Valid"
		
		if Coord[0] == "Valid":
			if self.piece_choisie == None:
				self.erreur.config(text="Vous devez choisir une pièce pour commencer !")
				# Cache le message d'erreur après un court délai
				self.after(1000, lambda:self.erreur.config(text=""))
				return

			# Si l'utilisateur a cliquer sur le plateau alors on esaye de placer la pièce
			try:
				self.board.placePiece(
					self.piece_choisie,
					Coord[1], Coord[2],
					color = self.cpt_tour)
			except PlacementException as e:
				# La pièce n'as pas pu être placée
				if self.parent.DEBUG:
					print("Erreur de placement : {}".format(e.args[0]))
				self.erreur.config(text=e.args[0])
				# Cache le message d'erreur après un court délai
				self.after(1000, lambda:self.erreur.config(text=""))
				return
			
			self.updateColors()
			# Passage au joueur suivant
			if self.cpt_tour == 1:
				self.cpt_tour = 2
				self.j1.config(relief=tk.FLAT)
				self.j2.config(relief=tk.SUNKEN)
			else:
				self.cpt_tour = 1
				self.j1.config(relief=tk.SUNKEN)
				self.j2.config(relief=tk.FLAT)
			
			# Vérifie si la partie est finie
			if self.board.isBoardFull():
				tk.messagebox.showinfo(
					"Victoire !",
					"Bravo ! Le joueur {} à remporté la partie.".format(self.cpt_tour))
			if self.parent.DEBUG:
				pprint.pprint(self.board.matrix)

	def reset(self):
		"""Replace tout le jeu à son état initial et relance une partie"""
		# Reset des variables
		self.piece_choisie = None
		self.listePieces = []
		self.cpt_tour = 1
		
		# Reset des canvas
		self.canvas.delete("all")
		self.tabpieces0.delete("all")
		self.tabpieces1.delete("all")
		self.tabpieces2.delete("all")

		# Reset de l'interface
		self.abandonner.config(state=tk.NORMAL)
		self.canvas.bind("<Button-1>", self.pointeur)

		# Re-init
		self.initBoard()
		self.initGrille()
		self.initChoix()


# Lancement du programme
if __name__ == "__main__":
	# Lancement du programme
	root = tk.Tk()
	app = FenetrePrincipale(root).pack(side="top", fill="both", expand=True)
	root.mainloop()