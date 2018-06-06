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
    return 'quote'

def getCommand ():
    return '/ilustrame'

def getRE ():
    return '/ilu*'

def getMade():
    webWiki = requests.get('http://www.proverbia.net/google/',proxies=proxies)
    webWiki.raise_for_status()
    webWiki.encoding = 'utf-8'
    soupWiki = bs4.BeautifulSoup(webWiki.text,'html.parser')
    author = soupWiki.title.string
    lineas = soupWiki.select('td [class="frasedeldia"]')
    frase = lineas[0].getText()
    autor = lineas[1].getText()
    return frase,autor
## fin de getQuote
