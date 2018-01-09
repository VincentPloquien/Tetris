#!/usr/bin/python3

# Dépendances
import random

# - Dépendances DEV
import pprint
pp = pprint.PrettyPrinter(indent=4)
# -

class Board:
	"""Le tableau de jeu d'une partie de Tetris avec sa bibliothèque de formes possibles"""
	def __init__(self, width, height, base=0):
		"""Initialise le tableau de jeu

		Keyword arguments:
		width -- la largeur du plateau
		height -- la hauteur du plateau
		base -- la valeur par défaut d'une case (défaut: 0)
		"""
		self.width = width
		self.height = height

		# Créer une matrice de taille width*height
		self.matrix = [[base]*width]*height

		# Créer une bibliothèques des formes possibles
		self.shapes = []

	# Gestion du plateau

	def fillMatrix(self, fillValue):
		"""Rempli le tableau de jeu avec la valeur fillValue"""
		for line in self.matrix:
			for element in line:
				element = fillValue

	def isEmpty(self, x, y):
		"""Renvoie True si la case en x,y est vide"""
		return self.matrix[y][x] == 0

	# Bibliothèques de pièces

	def addPiece(self, newPiece):
		"""Ajoute la pièce newPiece dans la bibliothèques des pièces possibles"""

		# Tests de validité
		if not isinstance(newPiece, Piece):
			raise ValueError("Le paramètre newPiece n'est pas un objet Piece")

		newShape = newPiece.shape
		if len(newShape) > self.height:
			raise ValueError("La hauteur d'une pièce ne peut pas être plus grande que celle du jeu")
		previousLength = -1
		for line in newShape:
			if len(line) > self.width:
				raise ValueError("La largeur d'une pièce ne peut pas être plus grande que celle du jeu")
			if len(line) != previousLength and previousLength != -1:
				raise ValueError("La largeur de la pièce n'est pas uniforme")
			previousLength = len(line)
			if not isinstance(line[0], int):
				raise ValueError("La pièce n'est pas constituée d'entiers")

		self.shapes.append(newPiece)

	def getRandomPiece(self):
		"""Renvoie une piece valide au hasard"""
		return random.choice(self.shapes)


class Piece:
	"""Une pièce de jeu, avec sa forme à elle"""
	def __init__(self, shape):
		"""Initialise la pièce

		Keyword arguments:
		shape -- tableau 2D décrivant la forme de la pièce
		"""
		self.shape = shape


if __name__=="__main__":
	board = Board(10,10)
	pp.pprint(board.matrix)
	board.addPiece(Piece([
			[1,1],
			[1,0]
	]))

	piece = board.getRandomPiece()
	pp.pprint(piece.shape)
