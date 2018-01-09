from tkinter import *
from tkinter.messagebox import *
largeur=500
hauteur=500
fenetre = Tk()
root = Tk.Tk() 
root.title('Tetris') 
ecran= Canvas(fenetre, width=largeur, height=hauteur)
texte=ecran.create_text(largeur/2, 10,  text="bienvenue")
ecran.pack()
def reset():
    ecran.itemconfig(texte,  text="la partie recommence avec les mêmes paramètres")
    ecran.pack()
def menu():
    ecran.itemconfig(texte,text="retour au menu principal")
    ecran.pack()
def petit():
     if askyesno('redémarrage', 'vous vous apprêtez à recommencer une nouvelle partie avec la taille petite, êtes vous sur?'):
        ecran.itemconfig(texte, text="la partie redémarre avec la taille choisie : petite")
def moyen():
    if askyesno('redémarrage', 'vous vous apprêtez à recommencer une nouvelle partie avec la taille moyenne, êtes vous sur?'):
     ecran.itemconfig(texte, text="la partie redémarre avec la taille choisie : moyenne")
def grand():
     if askyesno('redémarrage', 'vous vous apprêtez à recommencer une nouvelle partie avec la taille grande, êtes vous sur?'):
        ecran.itemconfig(texte, text="la partie redémarre avec la taille choisie : grande")
def quitter():
    if askyesno('attention', 'êtes vous sur de vouloir fermer la fenêtre?'):
        ecran.itemconfig(texte, text="confirmation de fermeture into fermeture de la fenetre")
        fenetre.destroy()
menubar = Menu(fenetre)
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Lancer une nouvelle partie", command=reset)
menu1.add_command(label="choir le mode de jeu", command=menu)
menu1.add_separator()
menu1.add_command(label="Quitter", command=quitter)
menubar.add_cascade(label="Menu", menu=menu1)
menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Petit", command=petit)
menu2.add_command(label="Moyen", command=moyen)
menu2.add_command(label="Grand", command=grand)
menubar.add_cascade(label="Taille du jeu", menu=menu2)
fenetre.config(menu=menubar)
fenetre.mainloop()
