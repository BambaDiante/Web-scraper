import requests
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'
}#ceci represente mon user agent car certaine application refue les requete dont les user agent son mal configure

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

url=(input("Veuillez renseigner le lien de la page que vous voulez scraper :"))

contenu=recuperer(url)

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




