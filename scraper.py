import requests
import sqlite3
from bs4 import BeautifulSoup


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
    try:

        page=requests.get(urlpage,headers=headers)
        contenu=BeautifulSoup(page.text, 'html.parser')
        return contenu

    except Exception as e:

        printf("Erreur sur votre page {urlpage}: {e}")
        return None
    
def get_all_pages(lien,nbres):

    urls=[]
    nbrepages=1
    for i in range(int(nbres)):

        i=f"{lien}{nbrepages}"
        nbrepages+=1
        urls.append(i)
    for i in range(len(urls)):

        try:
            page=requests.get(urls[i],headers=headers)
            contenu = BeautifulSoup(page.text, 'html.parser')
            urls[i]=contenu
        except Exception as e:
            print(f"Impossible de communiquer avec: {url[i]},erreur: {e}")

    return urls



def parse_content(url,selectername,selecterprice,selecterlink,srcimg,titre,prix,lien):

    titre=url.find_all(class_=selectername)
    for j in range(len(titre)):
        try:
            titre[j]=titre[j].text
            titre[j]=titre[j].strip()
        except Exception as e:
            print(f"Erreur: {e}")

    prix=url.find_all(class_=selecterprice)
    for j in range(len(prix)):
        try:
            prix[j]=prix[j].text
            prix[j]=nettoiprix(prix[j])
        except Exception as e:
            print(f"Erreur: {e}")

    for a in url.find_all(attrs={'class':selecterlink}):
        try:
            img=a.find('img')
            lien.append(img.get(srcimg))
        except Exception as e:
            print(f"Erreur: {e}")

    return(titre,prix,lien)

#min prends la longueur minimum car il ya des artciles qui n'ont pas de prix ou d'image chez expat-dakar
def affiche(titre, prix, lien):

    longueur = min(len(titre), len(prix), len(lien))
    for i in range(longueur):

        if titre[i] and prix[i] and lien[i]:

            print("Produit:", i)
            print("Titre:", titre[i])
            print("Prix:", prix[i])
            print("Lien:", lien[i])

#     print(prix)

def affecter(titre,prix,lien,category,source):

    Page=[]
    longueur = min(len(titre), len(prix), len(lien))
    for j in range(longueur):

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

reponse=input("Vous voulez scraper une ou plusieurs pages?(Tapez 1 si vous ne voulez scraper qu'une page): ")

if reponse=="1":

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
    CREATE TABLE IF NOT EXISTS electronique (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source VARCHAR NOT NULL,
        category VARCHAR NOT NULL,
        titre VARCHAR NOT NULL,
        prix INTEGER NOT NULL,
        lien VARCHAR NOT NULL
    )
    """)

    def enregistrer(Produits, table):

        i=input("Tapez 1 pour enregistrer vers la base de donnee: ")
        if i=="1":

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

    page=affecter(title,prix,lien,'electronique','expat-dakar')
    enregistrer(page,'electronique')
    db.close()

else:

    urldefault=input("Saisir l'url par defaut: ")
    nbres=input("Saisir le nombre de page a scraper : ")
    nbres=int(nbres)
    # urls=get_all_pages(urldefault,nbres)
    titre_final=[]
    prix_final=[]
    lien_final=[]

    sn=input("Veuillez entrer la class dans lequel on a le nom des produit: ")
    sp=input("Veuillez entrer la class dans lequel on a le prix des produit: ")
    sl=input("Veuillez entrer la class dans lequel on a l'image du produit: ")
    src=input("Saisir le selecteur dans lequel on a le lien de l'image du produit: ")

    for i in range(nbres):

        try:

            title=[]
            prix=[]
            lien=[]
            lien_temp=f"{urldefault}{i}"
            lien_temp=recuperer(lien_temp)
            title, prix, lien = parse_content(lien_temp, sn, sp, sl, src, title, prix, lien)
            titre_final.extend(title)
            prix_final.extend(prix)
            lien_final.extend(lien)

        except Exception as e:

            print(f"Erreur {e}")
            print(f"Le scrap s'arrete a la page {i}")
            break
    print("Affichage des informations du produit")
    affiche(titre_final,prix_final,lien_final)
    db = sqlite3.connect('database.db')
    # ceci est mon curseur il sert a executer des requetes dans ma base de donnees
    curseur = db.cursor()
    curseur.execute("""
    CREATE TABLE IF NOT EXISTS electronique(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source VARCHAR NOT NULL,
        category VARCHAR NOT NULL,
        titre VARCHAR NOT NULL,
        prix INTEGER NOT NULL,
        lien VARCHAR NOT NULL
        )
    """)

    def enregistrer(Produits, table):
        i = input("Tapez 1 pour enregistrer vers la base de donnee: ")
        if i == "1":
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


    page = affecter(titre_final, prix_final, lien_final, 'electronique', 'expat-dakar')
    enregistrer(page, 'electronique')
    db.close()