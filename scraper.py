import requests
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'
}#ceci represente mon user agent car certaine application refue les requete dont les user agent son mal configure
pagejumia=requests.get('https://www.jumia.sn/?srsltid=AfmBOoqajN71_PKpBHGCoakbDoq1Kqj-QqPG0Hu4ElhE4js9hrVHoeNq',headers=headers)
pageexpat=requests.get('https://www.expat-dakar.com/?gad_source=1&gad_campaignid=21566853061&gclid=Cj0KCQiA7fbLBhDJARIsAOAqhsfA9iJptSXXhg2KPm_YMmtKidQtoC57ivHUvy3Y5vLVIJ2A_4l2QbEaAlkVEALw_wcB',headers=headers)

contenujumia= BeautifulSoup(pagejumia.text, 'html.parser')#ici html parser specifie l'interpreteur que bs utilise
#page.text quant a lui represente la dom de jumia
contenuexpat= BeautifulSoup(pageexpat.text, 'html.parser')
imagesexpat=contenuexpat.find_all('img')

print(contenujumia)
print(contenuexpat)