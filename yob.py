import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

#importar el texto
    #hv de espanol
#hv = open('resume_es.txt', encoding="utf8")
    #hv en ingles
#hv = open('resume.txt')
#hv de espanol
hv = open('resume_es_2.txt', encoding="utf8")
hv = hv.read()
#1 Contar las palabras de la hoja de vida
wordcount = Counter(hv.split())
cont = 0
for item in wordcount.items():
    #imprime cada palabra y su frecuencia
    print("{}\t{}".format(*item))
    cont += item[1]
    #Extraer correo electronico
    if '@' in item[0]:
        email = item[0]
print('Total palabras ',cont)

#2 Extraer y verificar le numero y oorreo de contacto
print('Email ',email)
for i, item in enumerate(re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', hv)):
    print('Telefono', i+1, item)