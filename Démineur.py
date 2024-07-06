# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 21:04:05 2021

@author: alexa
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 07:54:36 2021

@author: boldoa
"""
from random import randint as ran
import tkinter as tk

import time
import threading

verrou = threading.Lock()
temps0 = time.monotonic()
fintemps = False

def horloge():
    der_temps = time.monotonic()
    while time.monotonic()-temps0 <= 999 and not fintemps:
        if time.monotonic()-1 > der_temps:
            der_temps = time.monotonic()
            verrou.acquire()
            label_heure.configure(text = "{}".format(int(time.monotonic()-temps0)))
            verrou.release()

def demineur(lig=10,col=10,ca=40, propbombes=0.2):
    global bombes
    global T_voisins
    global T_drapeau
    global bombe_decouverte
    global L
    global C
    global case
    global nb_bombes
    L = lig
    C = col
    case = ca
    bombes = [[0 for i in range(C)]for i in range(L)]
    nb_bombes = int(C*L*propbombes)
    n_bombes = nb_bombes
    while n_bombes !=0 :
        l_bombe = ran(0,L-1)
        c_bombe = ran(0,C-1)
        if bombes[l_bombe][c_bombe] != 1:
            bombes[l_bombe][c_bombe] = 1
            n_bombes -= 1
    T_voisins = trouver_voisins(bombes)
    T_drapeau = [[0 for i in range(C)]for i in range(L)]
    bombe_decouverte = 0
    creation_fenetre(L,C,case)
    
def trouver_voisins(bombes):
    T_voisins = [[0 for i in range(len(bombes[0]))]for i in range(len(bombes))]
    for l in range(len(bombes)):
        for c in range(len(bombes[l])):
            nb_voisins = 0
            if l > 0 :
                if bombes[l-1][c] == 1 :
                    nb_voisins += 1
                if c > 0 :
                    if bombes[l-1][c-1] == 1 :
                        nb_voisins += 1
                if c < len(bombes[l])-1:
                    if bombes[l-1][c+1] == 1 :
                        nb_voisins += 1
            if c > 0 :
                if bombes[l][c-1] == 1 :
                    nb_voisins += 1
            if c < len(bombes[l])-1:
                if bombes[l][c+1] == 1 :
                    nb_voisins += 1
            if l < len(bombes)-1:
                if bombes[l+1][c] == 1 :
                    nb_voisins += 1
                if c > 0 :
                    if bombes[l+1][c-1] == 1 :
                        nb_voisins += 1
                if c < len(bombes[l])-1:
                    if bombes[l+1][c+1] == 1 :
                        nb_voisins += 1
            T_voisins[l][c] = nb_voisins
    return T_voisins

def jouer(event):
    global tableau_chaine
    global T_drapeau
    x = event.x
    y = event.y
    for i in range(0, C):
        if x > (i+1)*case and x < (i+2)*case:
            c = i
    for j in range(0, L):
        if y > (j+1)*case and y < (j+2)*case :
            l = j
    if T_drapeau[l][c] == 1:
        pass
    elif bombes[l][c] == 1 :
        perdu()
    elif T_voisins[l][c] != 0 :
        apparaitre_case(c,l)
    else :
        tableau_chaine = [[0 for i in range(C)]for i in range(L)]
        recherche_chaine(l,c)
        for l in range(len(tableau_chaine)) :
            for c in range(len(tableau_chaine[0])):
                if tableau_chaine[l][c] == 1 and T_drapeau[l][c] == 0:
                    if l>0:
                        if tableau_chaine[l-1][c] == 0 and T_drapeau[l-1][c] == 0:
                            apparaitre_case(c,l-1)
                        if c>0:
                            if tableau_chaine[l-1][c-1] == 0 and T_drapeau[l-1][c-1] == 0:
                                apparaitre_case(c-1,l-1)
                        if c < C-1:
                            if tableau_chaine[l-1][c+1] == 0 and T_drapeau[l-1][c+1] == 0:
                                apparaitre_case(c+1,l-1)
                    if l < L-1:
                        if tableau_chaine[l+1][c] == 0 and T_drapeau[l+1][c] == 0:
                            apparaitre_case(c,l+1)
                        if c>0:
                            if tableau_chaine[l+1][c-1] == 0 and T_drapeau[l+1][c-1] == 0:
                                apparaitre_case(c-1,l+1)
                        if c < C-1:
                            if tableau_chaine[l+1][c+1] == 0 and T_drapeau[l+1][c+1] == 0:
                                apparaitre_case(c+1,l+1)
                    if c>0:
                        if tableau_chaine[l][c-1] == 0 and T_drapeau[l][c-1] == 0:
                            apparaitre_case(c-1,l)
                    if c < C-1:
                        if tableau_chaine[l][c+1] == 0 and T_drapeau[l][c+1] == 0:
                            apparaitre_case(c+1,l)
                    apparaitre_case(c,l)
    if nb_bombes-bombe_decouverte == 0:
        fin_de_partie()
      
def apparaitre_case(c,l):
    canva.create_rectangle((c+1)*case,(l+1)*case,(c+2)*case,(l+2)*case,fill="#B4B2A9", outline = "#8E8C84")
    canva.create_text ((c+1)*case+case//2,(l+1)*case+case//2, text = str(T_voisins[l][c]), fill = liste_couleurs[T_voisins[l][c]], font = police_chiffres)
              
def recherche_chaine(l,c):
    global tableau_chaine
    tableau_chaine[l][c] = 1
    if l>0:
        if tableau_chaine[l-1][c]==0 and T_voisins[l-1][c] == 0 and bombes[l-1][c] != 1:
            recherche_chaine(l-1,c)
        if c>0:
            if tableau_chaine[l-1][c-1]==0 and T_voisins[l-1][c-1] == 0 and bombes[l-1][c-1] != 1:
                recherche_chaine(l-1,c-1)
        if c < C-1:
            if tableau_chaine[l-1][c+1]==0 and T_voisins[l-1][c+1] == 0 and bombes[l-1][c+1] != 1:
                recherche_chaine(l-1,c+1)
    if l < L-1:
        if tableau_chaine[l+1][c]==0 and T_voisins[l+1][c] == 0 and bombes[l+1][c] != 1:
            recherche_chaine(l+1,c)
        if c>0:
            if tableau_chaine[l+1][c-1]==0 and T_voisins[l+1][c-1] == 0 and bombes[l+1][c-1] != 1:
                recherche_chaine(l+1,c-1)
        if c < C-1:
            if tableau_chaine[l+1][c+1]==0 and T_voisins[l+1][c+1] == 0 and bombes[l+1][c+1] != 1:
                recherche_chaine(l+1,c+1)
    if c>0:
        if tableau_chaine[l][c-1]==0 and T_voisins[l][c-1] == 0 and bombes[l][c-1] != 1:
            recherche_chaine(l,c-1)
    if c < C-1:
        if tableau_chaine[l][c+1]==0 and T_voisins[l][c+1] == 0 and bombes[l][c+1] != 1:
            recherche_chaine(l,c+1)

def DRAPEAU():
    global lie
    global bouton_DRAPEAU
    global bouton_REM_DRAP
    if lie == "jouer" or lie == "remove_drapeau":  
        canva.bind("<Button-1>", placer_drapeau)
        lie = "placer_drapeau"
        bouton_DRAPEAU.configure(relief ="sunken")
        bouton_REM_DRAP.configure(relief ="raised")
    else:
        canva.bind("<Button-1>", jouer)
        lie="jouer"
        bouton_DRAPEAU.configure(relief ="raised")
    
def placer_drapeau(event):
    global lie
    global T_drapeau
    global bombe_decouverte
    global label
    x = event.x
    y = event.y
    for i in range(0, C):
        if x > (i+1)*case and x < (i+2)*case:
            c = i
    for j in range(0, L):
        if y > (j+1)*case and y < (j+2)*case :
            l = j
    canva.create_oval((c+1)*case+case//3,(l+1)*case+case//3,(c+1)*case+2*case//3,(l+1)*case+2*case//3, fill = "red", outline = "red")
    T_drapeau[l][c] = 1
    bombe_decouverte += 1
    label.configure(text="Il reste {} bombes à découvrir".format(nb_bombes-bombe_decouverte))
    canva.bind("<Button-1>", jouer)
    lie="jouer"
    bouton_DRAPEAU.configure(relief ="raised")
    if nb_bombes-bombe_decouverte == 0:
        fin_de_partie()

def REM_DRAP():
    global lie
    global bouton_DRAPEAU
    global bouton_REM_DRAP
    if lie == "jouer" or lie == "placer_drapeau":  
        canva.bind("<Button-1>", remove_drapeau)
        lie = "remove_drapeau"
        bouton_DRAPEAU.configure(relief ="raised")
        bouton_REM_DRAP.configure(relief ="sunken")
    else:
        canva.bind("<Button-1>", jouer)
        lie="jouer"
        bouton_REM_DRAP.configure(relief ="raised")
        
def remove_drapeau(event):
    global lie
    global T_drapeau
    global bombe_decouverte
    global label
    x = event.x
    y = event.y
    for i in range(0, C):
        if x > (i+1)*case and x < (i+2)*case:
            c = i
    for j in range(0, L):
        if y > (j+1)*case and y < (j+2)*case :
            l = j
    canva.create_rectangle((c+1)*case,(l+1)*case,(c+2)*case,(l+2)*case,fill="#cdc8b7", outline="#aeaa9d")
    T_drapeau[l][c] = 0
    bombe_decouverte -= 1
    label.configure(text="Il reste {} bombes à découvrir".format(nb_bombes-bombe_decouverte))
    canva.bind("<Button-1>", jouer)
    lie="jouer"
    bouton_REM_DRAP.configure(relief ="raised")
    if nb_bombes-bombe_decouverte == 0:
        fin_de_partie()

def fin_de_partie():
    global label2
    global label3
    global bouton_OUI
    global bouton_NON
    label.place_forget()
    bouton_REM_DRAP.place_forget()
    bouton_DRAPEAU.place_forget()
    canva.bind("<Button-1>", PASSER)
    label2 = tk.Label(window, text="Vous avez marqué les potentiels emplacements de toutes les bombes")
    label2.place(x = 0, y = 0)
    label3 = tk.Label(window, text="Voulez-vous arrêter la partie ?")
    label3.place(x = 0, y = case)
    bouton_OUI = tk.Button(window,text="Oui", command=OUI_fin)
    bouton_OUI.place(x=case*(C-3)//2, y=case*2)
    bouton_NON = tk.Button(window,text="Non", command=NON_fin)
    bouton_NON.place(x=case*(C+6)//2, y=case*2)

def PASSER(event):
    pass

def OUI_fin():
    global fintemps
    label2.destroy()
    label3.destroy()
    bouton_OUI.destroy()
    bouton_NON.destroy()
    gagne = True
    for i in range(len(bombes)):
        for j in range(len(bombes[i])):
            if bombes[i][j] == 1:
                if T_drapeau[i][j] != 1 :
                    gagne = False
    if gagne :
        label4 = tk.Label(window, text="Vous avez trouvé toutes les bombes ! Bravo !")
        label4.place(x=0,y=0)
        fintemps = True
    else:
        perdu()

def NON_fin():
    label2.destroy()
    label3.destroy()
    bouton_OUI.destroy()
    bouton_NON.destroy()
    label.place(x = 0, y = 0)
    bouton_REM_DRAP.place(x=case*(C-3)//2, y=case*2)
    bouton_DRAPEAU.place(x=case*(C+6)//2, y=case*2)
    canva.bind("<Button-1>", jouer)
    
                
    
def perdu():
    global fintemps
    label.destroy()
    bouton_DRAPEAU.destroy()
    bouton_REM_DRAP.destroy()
    canva.bind("<Button-1>", PASSER)
    label4 = tk.Label(window, text="Vous avez perdu...")
    label4.place(x=0,y=0)
    fintemps = True
    for l in range(len(bombes)):
        for c in range(len(bombes[l])):
            if bombes[l][c] == 1:
                canva.create_rectangle((c+1)*case+case//6,(l+1)*case+case//6,(c+2)*case-case//6,(l+2)*case-case//6,fill="#AA0000", outline = "#FF0000")

def creation_fenetre(L,C,case):
    global window
    global bouton_DRAPEAU
    global bouton_REM_DRAP
    global canva
    global lie
    global bombe_decouverte
    global label
    global liste_couleurs
    global police_chiffres
    global label_heure
    police_chiffres = "impact"
    liste_couleurs = ["#B4B2A9","#1388D9","#29660E","#FF0000","#3C19A9","#611302","#0F7353","#DE980C","#5E003F"]
    window = tk.Tk()
    window.geometry("{}x{}".format(case*(C+4), case*(L+7))) 
    window.minsize(case*(C+4), case*(L+7))
    canva = tk.Canvas(window, bg="#cdc8b7", width=case*(C+2), height=case*(L+2))
    canva.place(x=case, y = 4*case)
    for i in range(L+1):
        canva.create_line(case, (i+1)*case, (C+1)*case+1, (i+1)*case, width=1, fill="#aeaa9d")
    for i in range(C+1):
        canva.create_line((i+1)*case, case, (i+1)*case, (L+1)*case+1, width=1, fill="#aeaa9d")
    canva.bind("<Button-1>", jouer)
    lie = "jouer"
    bouton_DRAPEAU = tk.Button(window,text="DRAPEAU", command=DRAPEAU) # voir ligne 253
    bouton_DRAPEAU.place(x=case*(C+6)//2, y=case*2)
    bouton_REM_DRAP = tk.Button(window,text="REMOVE DRAPEAU", command=REM_DRAP) # voir ligne 253
    bouton_REM_DRAP.place(x=case*(C-3)//2, y=case*2)
    label = tk.Label(window, text="Il reste {} bombes à découvrir".format(nb_bombes-bombe_decouverte))
    label.place(x = 0, y = 0)
    label_heure = tk.Label(text="000", font = ('Times New Roman',40))
    label_heure.place(x=case*C, y=case)
    window.mainloop()
    
def affiche(T):
    for i in range(len(T)):
        for j in range(len(T[i])):
            print("{:>3}".format(T[i][j]), end="")
        print("")
        
t1 = threading.Thread(target=horloge, args=[])
t2 = threading.Thread(target=demineur, args=[])
t1.start()
t2.start()
t1.join()
t2.join()