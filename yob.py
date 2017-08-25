import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re
from nltk.corpus import stopwords
from nltk.corpus.reader.plaintext import WordPunctTokenizer
from nltk.stem.snowball import SnowballStemmer
from nltk.probability import FreqDist
from collections import Counter
#este es un comentario de Daniel
def cleanDoc(doc):
    stopset = set(stopwords.words('spanish'))
    stemmer = SnowballStemmer('spanishS')
    tokens = WordPunctTokenizer().tokenize(doc)
    clean = [token.lower() for token in tokens if token.lower() not in stopset and len(token) > 2]
    final = [stemmer.stem(word) for word in clean]
    return final

#importar el texto
hv = open('resume_es.txt', encoding="utf8")
#hv = open('resume_es_2.txt', encoding="utf8")

#Empleos
job = open('empleo_ing_geol.txt', encoding="ANSI")

#--------------------------------------
hv = hv.read()
job = job.read()
#1 Contar las palabras de la hoja de vida
wordcount = Counter(hv.split())
cont = 0
email=[]
for item in wordcount.items():
    #imprime cada palabra y su frecuencia
    print("{}\t{}".format(*item))
    cont += item[1]
    #Extraer correo electronico
    if '@' in item[0]:
        email.append(item[0])

print('Total palabras ',cont)

#2 Extraer y verificar le numero y oorreo de contacto usando ReGex (Regular expressions)
print('Email',email)
for i, item in enumerate(re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', hv)):
    print('Telefono', i+1, item)

#3
# job_description --> senior product leader

#4 Hard skills http://graus.co/thesis/string-similarity-with-tfidf-and-python/
test_hv = cleanDoc(hv)
#print (test_hv)
counts = Counter(test_hv)

#dist = FreqDist(counts)
#imprime grafico de frecuencias de keywords
#dist.plot(10)
print ('Keywords de la HV : ', counts.most_common(20))

#--------------------------------------

test_job = cleanDoc(job)
#print (test_job)
counts = Counter(test_job)

#dist_job = FreqDist(counts)
#imprime grafico de frecuencias de keywords
#dist_job.plot(10)
print ('Keywords de la oferta : ', counts.most_common(20))

inter = set(test_hv) & set(test_job)
#inter = hv & job
print ('Intersección de keywords entre oferta y HV ', inter)