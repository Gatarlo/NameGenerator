import pandas as pd
import random
#nom du csv de r�f�rence et de la colonne choisie comme base
#filename = "communes-01042019.csv"
#colonne = 'nccenr'
filename = "Light_Novels.txt"
colonne = 'title'
poids = 4
longueur_max = 10
nombreVoulu = 20

#Lecture du csv
with open(filename, 'r', encoding='ISO-8859-1') as csvfile: 
    # cr�ation d'un objet "reader"'
    csvreader = pd.read_csv(csvfile, sep='|') 

#Fonction de s�lection des prochaines lettres en fonction de leur nombre d'occurences
def Markov(data, n): #fonction de cr�ation des listes de tuples
    liste = {
        '_initial':{}, #dictionnaire contenant les n premi�res lettres de chaque villages et leurs occurences'
        '_village': set(data) #set(data) correspond � la liste de village donn�e dans csvreader
    }
    for mot in data: #le mot est le village actuellement s�lectionn� dans la liste
        entourageMot = str(mot) + '.'
        for i in range(0, len(entourageMot) - n):
            tuple = entourageMot[i:i + n] #un tuple est un groupe de n lettres, ici les premi�res du village
            next = entourageMot[i + 1:i + n + 1] #on d�cale de 1, ici la suite de n lettres a partir de la seconde lettre
            
            if tuple not in liste:
                entree = liste[tuple] = {} #entr�e est la liste des tuples peu importe leur position
            else:
                entree = liste[tuple]
            
            if i == 0:
                if tuple not in liste['_initial']: #on cr�e une occurence au tuple d'initial s'il n'existe pas d�j� (uniquement si il est le premier tuple)
                    liste['_initial'][tuple] = 1 
                else: #on ajoute une occurence au tuple d'initial s'il existe
                    liste['_initial'][tuple] += 1
                    
            if next not in entree: 
                entree[next] = 1 #meme fonction qu'au dessus mais pour chaque tuple autre que les tuples de d�part
            else:
                entree[next] += 1
    return liste  

def selection_aleatoire(items): #items est la liste de tuples donn�e () 
    rnd = random.random() * sum(items.values()) #on multiplie un nombre al�atoire par la somme des occurences des tuples
    for item in items: # pour chaque tuple on soustrait son index au nombre al�atoire
        rnd -= items[item]
        if rnd < 0: #Le tuple sur lequel le nombre al�atoire passe en dessous de z�ro est renvoy�
            return item

def generate(liste):
    tuple = selection_aleatoire(liste['_initial']) #S�lection du tuple initial
    result = [tuple]
    
    while True:
        tuple = selection_aleatoire(liste[tuple]) #S�lection des tuples suivant jusqu'� ce qu'une condition d'arr�t soit rencontr�e
        last_character = tuple[-1] #on prend l'avant dernier caract�re du tuple, ce sera le dernier du village si une condition d'arr�t est rencontr�e
        if last_character == '.': #si le caract�re d'un tuple est "." on brise la boucle 
            break
        if last_character == ' ' and result.count(' ') == 9 : #si le caract�re d'un tuple est " " on brise la boucle         
            break 
#        if last_character == '-' and result.count('-') == 3 : #trois '-' max suffisent amplement, on brise avant de d�passer
#            break 
#        if len(result) > longueur_max: #limite de taille
#            break
        result.append(last_character) #on ajoute le dernier caract�re au nom de village.
        
    
    generated = ''.join(result)
    if generated not in liste['_village']: #on v�rifie que le nom n'existe pas d�j� dans la liste de villages
        return generated
    else:
        return generate(liste)

def Generer(nombre): #choix du nombre de village que l'on veut g�n�rer
    liste = Markov(csvreader[colonne].tolist(), poids) #colonne de r�f�rence et nombre de nombre de poids
    return [generate(liste) for _ in range(nombre)]

print('\n'.join(Generer(nombreVoulu)))