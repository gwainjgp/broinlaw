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



# Para manejar las expresiones regulares
import re

# para obtener la frase 
import requests,bs4
proxies = {
  'http': proxy_url,
  'https': proxy_url,
}
import broknow
from broknow import *;
actionsBro = broknow.__all__
#print 'Test: {0}'.format(eval(actionsBro[0]).getName())
#print 'Test: {0}'.format(quote.getMade())

for i in actionsBro:
    print u'# El turno de la función i es: {0}'.format(i)
    print u'  Name: {0}'.format(eval(i).getName())
    print u'   Command: {0}'.format(eval(i).getCommand())
    print u'   RE: {0}'.format(eval(i).getRE())
    print u'   Mensaje :{0}'.format(eval(i).getMade())


# importamos los modulos

