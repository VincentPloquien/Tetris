from tkinter import *

LARG = 6    #Largeur de la grille (a remplacer par Board.width)
HAUT = 6    #Hauteur de la grille (a remplacer par Board.height)
PIX_H_INTERFACE = 200   #Place pour le reste des trucs
PIX_L_INTERFACE = 400   #Place pour le reste des trucs

Tableau = [
    [0,1,0,1,1,1],
    [1,1,1,0,2,2],
    [0,1,1,1,2,2],  #Temporaire "1" = J1 | "2" = J2
    [1,1,1,0,2,2],
    [0,1,0,0,0,0],
    [0,0,0,0,0,0],
    ]
TAILLE_CARREAU = 25 #Coté de chaque carreau de la grille en pixel

#====== Génération de la grille ======
def initGrille():
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
    for i in range(LARG):
        for j in range(HAUT):
            if (Tableau[j][i] == 1) :
                tag = str(i)+"-"+str(j)
                C = canvas.find_withtag(tag)
                canvas.itemconfigure(C, fill = "green")
            if (Tableau[j][i] == 2) :
                tag = str(i)+"-"+str(j)
                C = canvas.find_withtag(tag)
                canvas.itemconfigure(C, fill = "red")
#====== Fonciton qui cherche où l'on clique ======
def pointeur(event):
    Coord = []
    if (event.x > PIX_L_INTERFACE/2 and event.x < PIX_L_INTERFACE/2+LARG*TAILLE_CARREAU):
        X_Carreau = abs((event.x - PIX_L_INTERFACE/2))//TAILLE_CARREAU
        print(X_Carreau)
    if (event.y > PIX_H_INTERFACE/2 and event.y < PIX_H_INTERFACE/2+HAUT*TAILLE_CARREAU):
        Y_Carreau = abs(((PIX_H_INTERFACE+HAUT*TAILLE_CARREAU-event.y) - PIX_H_INTERFACE/2)//TAILLE_CARREAU)
        print(Y_Carreau)

fenetre = Tk()

label = Label(fenetre, text="Tétriste")
label.grid()

canvas = Canvas(fenetre, width=(PIX_L_INTERFACE+LARG*TAILLE_CARREAU), height=(PIX_H_INTERFACE+HAUT*TAILLE_CARREAU), background='white') #Board.widthm Board.height
initGrille()
find()
canvas.bind("<Button-1>", pointeur)

canvas.grid()

fenetre.mainloop()

