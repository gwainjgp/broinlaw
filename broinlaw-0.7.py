#!/usr/bin/env python2.7
# -*- coding: utf-8 -*

import time
import random
import datetime
import telepot


## Para usar proxy
import urllib3
import telepot.api
proxy_url = 'http://10.82.0.173:8080'
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

# Activamos el log
import logging,sys
logfile = 'log-' + 'broinlaw' + '.log'
logging.basicConfig(filename=logfile,level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
logging.debug('Arrancamos a al cuñao...')

# Para manejar las expresiones regulares
import re

# para obtener la frase 
import requests,bs4
proxies = {
  'http': proxy_url,
  'https': proxy_url,
}

## Conectamos con proverbia.net 
def getQuote():
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


## adquirir y enviar una foto bonica
def getFotoBonica():
    webFoto = requests.get('https://commons.wikimedia.org/wiki/Special:Random/File', proxies=proxies)
    webFoto.raise_for_status()
    webFoto.encoding = 'utf-8'
    soupFoto = bs4.BeautifulSoup(webFoto.text,'html.parser')
    elementoFoto = soupFoto.select('#file img')
    if elementoFoto == []:
        print('No encuentro la foto.')
        urlFoto = 'https://species.wikimedia.org/wiki/Felis_silvestris_catus#/media/File:Felis_catus-cat_on_snow.jpg'
    else:
        urlFoto = elementoFoto[0].get('src')
    return urlFoto


# masters = [299567175,12602564]
TOKEN = '351657423:AAGoqTe9HpfNy-NDv1mUOmi6Q0OP8OHmdc8'



## abonados
#fichero de abonados - persistencia
import io,json
fichero_abonados = './abonados.json'
Abonados = []
with open(fichero_abonados) as datos_abonados:
    try:
        Abonados = json.load(datos_abonados)
        logging.debug('Leyendo fichero de abonados'.format(fichero_abonados))
        datos_abonados.close()
    except:
        logging.debug('No existe el fichero de abonados'.format(fichero_abonados))
def save_abonados(abonados,fichero): 
    with io.open(fichero_abonados, 'w', encoding='utf8') as outfile:
        str_ = json.dumps(abonados, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
        outfile.write(unicode(str_))
        outfile.close()

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    master_name = msg['chat']['first_name']
    logging.debug('Chat ID: {0}'.format(chat_id))
    logging.debug('Master name: {0}'.format(master_name))
    logging.debug('Got command: {0}'.format(command))
    if re.search('/unir.*',command,re.IGNORECASE):
        if (chat_id not in Abonados):
            logging.debug('Apuntando a {0}'.format(chat_id))
            Abonados.append(chat_id)
            bot.sendMessage(chat_id, 'Sabes lo que quieres, {}, y ahoras serás más listo'.format(master_name))
            save_abonados(Abonados,fichero_abonados)
            logging.debug('Se guarda a {0} en el fichero de abonados'.format(chat_id))
        else:
            bot.sendMessage(chat_id, 'Ya estabas apuntado, {}. No te pases de listo'.format(master_name))
    elif re.search('/adi.*',command,re.IGNORECASE):
        if (chat_id in Abonados):
            logging.debug('Borrando a {0}'.format(chat_id))
            Abonados.remove(chat_id)
            bot.sendMessage(chat_id, 'Tu te lo pierdes, {}.'.format(master_name))
        else:
            bot.sendMessage(chat_id, 'No estabas apuntado, {}. No te pases de listo'.format(master_name))
    
    elif re.search('/ilu.*',command,re.IGNORECASE):
        logging.debug('Runing /ilustrame')
        cita,autor = getQuote()
        bot.sendMessage(chat_id, cita, parse_mode='HTML')
        bot.sendMessage(chat_id, u'\nque no lo digo yo, que lo dijo <b>' + autor + u'</b>', parse_mode='HTML')   
    elif re.search('/asom.*',command,re.IGNORECASE):
       logging.debug('Runing /asombrame')
       urlfoto = getFotoBonica()
       logging.debug('Foto seleccionada {0}'.format(urlfoto))
       bot.sendMessage(chat_id, u'<b>Foto del Cuñado</b>\n Mira que <a href="' + urlfoto + u'">fotico</a> tan bonica he encontrado' , parse_mode='HTML')
    ## A partir de aqui ayudas
    elif re.search('/help\Z',command,re.IGNORECASE):
       logging.debug('Running /help')
       ayuda ='''
Esto es lo que puedo hacer por ti, prenda:
   /ilustrame -> te deslumbro con mi sabiduría
   /asombrame -> te mando una foto bonica
   /unirme -> te deslumbraré periódicamente con mi sapiencia
   /adios -> te borro de la lista
'''
       bot.sendMessage(chat_id, ayuda)
       # No entiendo la orden
    else:
       bot.sendMessage(chat_id, '¿Qué me dices?\nMira a ver con /help')
       bot.sendMessage(chat_id, u'\U0001F613')
# Arrancando
bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('El cuñao lo sabe todo...')
logging.debug('El cuñao lo sabe todo...')
acciones = ['frase','foto']
nextTime = time.time()
pesadez = 3600
while 1:
    time.sleep(10)
    # Si hay abonados
    if ((Abonados) and (time.time() > nextTime)):
        logging.debug('Atendemos a los clientes')
        toca = random.choice(acciones)
        if (toca == 'frase'):
            frasedelMomento, autordelMomento = getQuote()
            for person in Abonados:
                logging.debug('Mandando mensaje a: {0}'.format(person))
                #bot.sendMessage(person, '@broinlaw_bot ' + frasedelMomento)
                try:
                    bot.sendMessage(person, u'<b>Frase del Cuñado</b>\n' + frasedelMomento + u'\nQue no lo digo yo, que lo dijo <b>' + autordelMomento + u'</b>', parse_mode='HTML')
                except:
                    logging.debug('Problemas mandando mensaje a {0}'.format(person))   
        elif (toca == 'foto'):
            urlfotodelmomento = getFotoBonica()
            for person in Abonados:
                logging.debug('Mandando foto a: {0}'.format(person))
                try:
                    bot.sendMessage(person, u'<b>Foto del Cuñado</b>\n Una <a href="' + urlfotodelmomento + u'">fotico</a> bonica bonica para animarte' , parse_mode='HTML')
                except:
                    logging.debug('Problemas mandando foto a {0}'.format(person))
        else:
            logging.debug('WARNING: Accion de atencion al usuario no definada')        
        nextTime = time.time() + pesadez + random.randint(1,pesadez)
        logging.debug('siguiente mensaje en time: {0}'.format(nextTime))
        

