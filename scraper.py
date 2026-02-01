import requests
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'
}#ceci represente mon user agent car certaine application refue les requete dont les user agent son mal configure
pagejumia=requests.get('https://www.jumia.sn/',headers=headers)
pageexpat=requests.get('https://www.expat-dakar.com/',headers=headers)

contenujumia= BeautifulSoup(pagejumia.text, 'html.parser')#ici html parser specifie l'interpreteur que bs utilise
#page.text quant a lui represente la dom de jumia
contenuexpat= BeautifulSoup(pageexpat.text, 'html.parser')
imagesexpat=contenuexpat.find_all('img')


modejumia=requests.get('https://www.jumia.sn/fashion-mode/',headers=headers)
modejumia=BeautifulSoup(modejumia.text, 'html.parser')

modehommeexpat1=requests.get("https://www.expat-dakar.com/vetements-homme/",headers=headers)
modehommeexpat2=requests.get("https://www.expat-dakar.com/chaussures-homme/",headers=headers)
modefemme1expat=requests.get("https://www.expat-dakar.com/vetements-femme",headers=headers)
modefemme2expat=requests.get("https://www.expat-dakar.com/chaussures-femme",headers=headers)
modeexpat=requests.get("https://www.expat-dakar.com/accessoires-de-mode/",headers=headers)
modehommeexpat2=BeautifulSoup(modehommeexpat2.text, 'html.parser')
modeexpat=BeautifulSoup(modeexpat.text, 'html.parser')
modefemme1expat=BeautifulSoup(modefemme1expat.text,'html.parser')
modefemme2expat=BeautifulSoup(modefemme2expat.text, 'html.parser')

# print(modeexpat)
# print(modefemme1expat)
# print(modefemme2expat)
# print(modehommeexpat1)
# print(modehommeexpat2)
# print(contenujumia)
#Je vais maintenant creer des dictionnaires contenant les informations concernant les produit de mode de jumia
jumiamode=[]

nbreprod=len(contenujumia.find_all(class_='name'))
# print(nbreprod)
title=contenujumia.find_all(class_='name')
for i in range(len(title)):
    title[i]=title[i].text
price=contenujumia.find_all(class_='prc')
for i in range(len(price)):
    price[i]=price[i].text
for i in range(nbreprod):
    jumiamode.append({'title': title[i], 'price': price[i]})
for i in range(nbreprod):
    print("Product: ",i+1)
    print("Title: ",jumiamode[i]['title'])
    print("Price: ",jumiamode[i]['price'])