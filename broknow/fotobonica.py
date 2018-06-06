# coding=utf-8
#
# Obtengo una cita para el cuñao
#

import requests,bs4

## Para usar proxy
proxy_url = 'http://10.82.0.173:8080'
proxies = {
  'http': proxy_url,
  'https': proxy_url,
}
# funciones publicas
def getName ():
    return 'fotoBonica'

def getCommand ():
    return '/asombrame'

def getRE ():
    return '/asom*'

def getMade():
    webFoto = requests.get('https://commons.wikimedia.org/wiki/Special:Random/File', proxies=proxies)
    webFoto.raise_for_status()
    webFoto.encoding = 'utf-8'
    soupFoto = bs4.BeautifulSoup(webFoto.text,'html.parser')
    elementoFoto = soupFoto.select('#file img')
    if elementoFoto == []:
        print('No encuentro la foto.')
        urlfoto = 'https://species.wikimedia.org/wiki/Felis_silvestris_catus#/media/File:Felis_catus-cat_on_snow.jpg'
    else:
        urlfoto = elementoFoto[0].get('src')
    msg =u'<b>Foto del Cuñado</b>\n Mira que <a href="' + urlfoto + u'">fotico</a> tan bonica he encontrado' 
    return msg 
## fin de getQuote
