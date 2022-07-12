#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk
import time

# creation du graphe principal avec les numeros de sommets et les distances qui lui sont associées:

with open("distance.txt", "r") as file:
    lines = file.readlines()
    graphe = {n: {} for n in range(0, 376)}
    for line in lines:
        a = line.split()

        if a[0] == "E":
            graphe[int(a[1])][int(a[2])] = int(a[3])
            graphe[int(a[2])][int(a[1])] = int(a[3])


with open("station.txt", "r") as file:
    lines = file.readlines()
    metro = {n: {} for n in range(0, 376)}
    for line in lines:
        a = line.split()

        if a[0] == "V":
            metro[int(a[1])] = " ".join(a[2::])


sommet = graphe.keys()

l = ["M1", "M2", "M3", "M3bis", "M4", "M5", "M6", "M7",
     "M7bis", "M8", "M9", "M10", "M11", "M12", "M13", "M14"]


with open("metro.txt", "r") as file:
    lines = file.readlines()
    ligne = {}
    for line in lines:
        a = line.split()
        for i in range(len(l)):
            if l[i] in a:
                ligne[((int(a[1])))] = l[int(i)]


dico = {}
for k, v in ligne.items():
    dico[v] = dico.get(v, []) + [k]
sommet = graphe.keys()


# fonction qui donne les sommets auquelle est relie un sommet


def liste_adjacence_sommet(sommet):
    return(graphe[sommet])

# fonction qui montre si il existe un chemin entre deux sommets


def Existe_chemin(graphe, sommet1, sommet2):

    for i in liste_adjacence_sommet(sommet1):
        if sommet2 == i:
            return True

        elif graphe[sommet1] == sommet2:
            return True

    return False


# Existe_chemin(graphe, 159, 0)


# Fonction graphe non orienté :


def connecte(graphe):
    n = len(sommet)  # nombre de sommets
    for sommet1 in range(n):
        for sommet2 in graphe[sommet1]:
            if Existe_chemin(graphe, sommet2, sommet1) == False:
                return False

    return True


def connecte1(graphe):
    n = len(sommet)  # nombre de sommets
    for sommet2 in range(n):
        for sommet1 in graphe[sommet2]:
            if Existe_chemin(graphe, sommet2, sommet1) == False:
                return False

    return True


# fonction graphe orienté :


def graphe_connexe(graphe):
    if connecte1(graphe) == connecte(graphe):
        return True
    else:
        return False

# fonction qui permet de recuperer le nom de la station d'arrivee en fonction de son numero


def get_number(name1):
    L = []
    for key, value in metro.items():
        if name1 == value:
            L.append(key)
    return L


# fonction qui permet de recuperer le numero de la station de depart en fonction de son numero


def get(name1):
    for key, value in metro.items():
        if name1 == key:
            return value


def convertion(seconde):
    return time.strftime("%M:%S", time.gmtime(seconde))


# fonction qui donne la distance entre deux sommets ainsi que son parcours


def detail_chemin():
    d = departchoisi.get()
    lst1 = [i[0] for i in variable if i[0] == d]
    init = " " . join(lst1)
    a = arriveechoisi.get()
    lst = [i[0] for i in variable if i[0] == a]
    final = " " . join(lst)
    depart = get_number(init)
    arrivee = get_number(final)
    dep, arr = station(graphe, depart, arrivee)
    distance, chemin = dijkstra(graphe, dep, arr)
    print("Vous etes actuellement a {}".format(init))
    numero_ligne = parcours_liste(dep)
    print("Prenez la ligne {} direction {}".format(
        numero_ligne, get(direction(numero_ligne, depart[0], arrivee[0]))))

    for ele in chemin:
        a = parcours_liste(ele)
        if numero_ligne != a:
            numero_ligne = a
            print("A {} changer et prenez la ligne {} direction {}".format(
                get(ele), numero_ligne, get(direction(numero_ligne, depart[0], arrivee[0]))))
    print("Vous devriez arrivee a {} dans {} minutes".format(
        final, convertion(distance)))


def dijkstra2(graphe, depart, arrivee, terminus):
    precedent = {x: None for x in graphe.keys()}
    dejaTraite = {x: False for x in graphe.keys()}
    distance = {x: float('inf') for x in graphe.keys()}
    distance[terminus] = 0
    a_traiter = [(0, terminus)]
    while a_traiter:
        dist_noeud, noeud = a_traiter.pop()
        if not dejaTraite[noeud]:
            dejaTraite[noeud] = True
            for voisin in graphe[noeud].keys():
                dist_voisin = dist_noeud + graphe[noeud][voisin]
                if dist_voisin < distance[voisin]:
                    distance[voisin] = dist_voisin
                    precedent[voisin] = noeud
                    a_traiter.append((dist_voisin, voisin))
        a_traiter.sort(reverse=True)
    a = distance[depart] - distance[arrivee]
    return a


def dijkstra(graphe, source, arrivee):

    precedent = {x: None for x in graphe.keys()}
    dejaTraite = {x: False for x in graphe.keys()}
    distance = {x: float('inf') for x in graphe.keys()}
    distance[source] = 0
    a_traiter = [(0, source)]
    while a_traiter:
        dist_noeud, noeud = a_traiter.pop()
        if not dejaTraite[noeud]:
            dejaTraite[noeud] = True
            for voisin in graphe[noeud].keys():
                dist_voisin = dist_noeud + graphe[noeud][voisin]
                if dist_voisin < distance[voisin]:
                    distance[voisin] = dist_voisin
                    precedent[voisin] = noeud
                    a_traiter.append((dist_voisin, voisin))
        a_traiter.sort(reverse=True)

    itin = []
    station = arrivee
    while True:
        if station == None:
            break
        itin.append(station)
        station = precedent[station]

    return distance[arrivee], itin


def station(graphe, depart, arrivee):
    """Prend les stations depart et arrivée en string et trouve la meilleure ligne à prendre de depart puis appliquer la fonction de Dijkstra"""
    sta = []
    for dep in depart:
        for a in arrivee:
            d, chemin = dijkstra(graphe, a, dep)
            sta.append([d, a, dep])
    resultat = min(sta)
    return resultat[2], resultat[1]


Destination = {24: 'M3 bis', 28: 'M5', 37: 'M10', 57: 'M6', 66: 'M1', 68: 'M11', 72: 'M13', 89: 'M8', 112: 'M13', 114: 'M3', 116: 'M3 bis', 117: 'M10', 130: 'M1', 152: 'M7', 170: 'M7 bis', 176: 'M3 bis',
               178: 'M12', 179: 'M7', 181: 'M9', 183: 'M11', 213: 'M2', 214: 'M6', 240: 'M8', 242: 'M5', 251: 'M3', 253: 'M9', 256: 'M2', 262: 'M4', 268: 'M4', 276: 'M12', 279: 'M3 bis', 319: 'M13', 363: 'M7'}


def direction(numero_ligne, depart, arrivee):
    l = []
    L2 = []
    for i, j in Destination.items():
        if j == numero_ligne:
            l.append(i)
    for i in l:
        d = dijkstra2(graphe, depart, arrivee, i)
        L2.append([d, i])
    return min(L2)[1]


def parcours_liste(sommet):
    for key, value in dico.items():
        if sommet in value:
            return key


if __name__ == "__main__":
    print(graphe_connexe(graphe))

# dijsktra : plus court chemins

# Fenetre graphique

Couleurs = ["yellow", "navy", "OliveDrab4", "CadetBlue1", "magenta4", "DarkOrange2",
            "PaleGreen3", "PaleVioletRed1", "SpringGreen2", "MediumPurple1", "OliveDrab2",
            "goldnrod1", "brown", "dark green", "turquoise2", "DarkOrchid4"]

with open("station.txt", "r") as tf:
    lines = tf.readlines()
    liste = []
    liste2 = []
    for line in lines:
        liste.append(line.split()[2::])
    for i in liste:
        if i not in liste2:
            liste2.append(i)


OptionList = liste2

app = tk.Tk()

app.title("METRO")

app.iconphoto(False, tk.PhotoImage(file='Logo-RATP-1.png'))

app.geometry('500x400')
app.configure(bg='snow')


# label

ttk.Label(app, text="Trouvez votre itineraire",
          background='sea green', foreground="white",
          font=("Times New Roman", 15)).grid(row=0, column=1)

ttk.Label(app, text=" Choisir la station de départ :",
          background='sea green', foreground="white",
          font=("Times New Roman", 10)).grid(column=0,
                                             row=5, padx=10, pady=25)

ttk.Label(app, text=" Choisir la station d'arrivée :",
          background='sea green', foreground="white",
          font=("Times New Roman", 10)).grid(column=0,
                                             row=7, padx=10, pady=25)

ttk.Label(app, text=" Choisir la station d'arrivée :",
          background='sea green', foreground="white",
          font=("Times New Roman", 10)).grid(column=0,
                                             row=7, padx=10, pady=25)


variable = tk.StringVar(app)
variable = OptionList

departchoisi = ttk.Combobox(app, width=27)
departchoisi['values'] = variable


departchoisi.grid(column=1, row=5)
d = departchoisi.current(0)


arriveechoisi = ttk.Combobox(app, width=27, textvariable=variable)
arriveechoisi['values'] = variable

arriveechoisi.grid(column=1, row=7)
arriveechoisi.current(1)


# bouton

bt = ttk.Button(app, text="Chercher", command=detail_chemin)
bt.grid(row=10, column=1)


app.mainloop()
