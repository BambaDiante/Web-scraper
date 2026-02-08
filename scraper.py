import requests
import sqlite3
from bs4 import BeautifulSoup
from unicodedata import category

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'
}#ceci represente mon user agent car certaine application refue les requete dont les user agent son mal configure

def nettoiprix(prix_texte):
    chiffres = ""
    for caractere in prix_texte:
        if caractere.isdigit():
            chiffres = chiffres + caractere
    if chiffres != "":
        return int(chiffres)
    else:
        return 0
def recuperer(urlpage):

    page=requests.get(urlpage,headers=headers)
    contenu=BeautifulSoup(page.text, 'html.parser')
    return contenu


def parse_content(url,selectername,selecterprice,selecterlink,srcimg,titre,prix,lien):

    titre=url.find_all(class_=selectername)
    for j in range(len(titre)):
        titre[j]=titre[j].text

    prix=url.find_all(class_=selecterprice)
    for j in range(len(prix)):
        prix[j]=prix[j].text
        prix[j]=nettoiprix(prix[j])

    for a in url.find_all(attrs={'class':selecterlink}):
        img=a.find('img')
        lien.append(img.get(srcimg))
    return(titre,prix,lien)

#
def affiche(titre,prix,lien):
    for i in range (len(titre)):
        print("Produit: ",i)
        print("Titre: ",titre[i])
        print("Prix: ",prix[i])
        print("Lien: ",lien[i])
        i=i+1
# def afficher(prix):
#     print(prix)

def affecter(titre,prix,lien,category,source):
    Page=[]
    for j in range(len(titre)):
        if (titre[j]!="") and (prix[j]!=0) and (lien[j]!=""):
            produit={
                'source':source,
                'categorie':category,
                'titre':titre[j],
                'prix':prix[j],
                'lien':lien[j],
            }
            Page.append(produit)
    print("Informations affecte a la page avec succes")
    return Page


url=(input("Veuillez renseigner le lien de la page que vous voulez scraper :"))

contenu=recuperer(url)
page=[]
title=[]
prix=[]
lien=[]
sn=input("Veuillez entrer la class dans lequel on a le nom des produit: ")
sp=input("Veuillez entrer la class dans lequel on a le prix des produit: ")
sl=input("Veuillez entrer la class dans lequel on a l'image du produit: ")
src=input("Saisir le selecteur dans lequel on a le lien de l'image du produit: ")

title,prix,lien=parse_content(contenu,sn,sp,sl,src,title,prix,lien)

print("Affichage des informations du produit")

affiche(title,prix,lien)
#creer ou ouvir le fichier de la base de donnee
db=sqlite3.connect('database.db')
#ceci est mon curseur il sert a executer des requetes dans ma base de donnees
curseur=db.cursor()

curseur.execute("""
CREATE TABLE IF NOT EXISTS divers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source VARCHAR NOT NULL,
    category VARCHAR NOT NULL,
    titre VARCHAR NOT NULL,
    prix INTEGER NOT NULL,
    lien VARCHAR NOT NULL
)
""")

def enregistrer(Produits, table):
    for i in range(len(Produits)):
        curseur.execute(f"INSERT INTO {table} (source, category, titre, prix, lien) VALUES (?,?,?,?,?)",
            (
                Produits[i]['source'],
                Produits[i]['categorie'],
                Produits[i]['titre'],
                Produits[i]['prix'],
                Produits[i]['lien']
            ))
    db.commit()
    print("Informations enregistrees avec succes")

page=affecter(title,prix,lien,'divers','jumia')
enregistrer(page,'divers')
