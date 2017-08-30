import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re
from nltk.corpus import stopwords
from nltk.corpus.reader.plaintext import WordPunctTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import time

inicio = time.time()


def cleanDoc(doc):
    stopset = set(stopwords.words('spanish'))
    #stemmer = PorterStemmer('spanish')
    stemmer = SnowballStemmer('spanish')
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
    #print("{}\t{}".format(*item))
    cont += item[1]
    #Extraer correo electronico
    if '@' in item[0]:
        email.append(item[0])

#print('Total palabras ',cont)

#2 Extraer y verificar le numero y oorreo de contacto usando ReGex (Regular expressions)
#print('Email',email)
tel = []
for i, item in enumerate(re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', hv)):
    tel.append(item)
#print (tel)
#3
# job_description --> senior product leader

#4 Hard skills http://graus.co/thesis/string-similarity-with-tfidf-and-python/
test_hv = cleanDoc(hv)
#print (test_hv)
counts = Counter(test_hv)

#dist = FreqDist(counts)
#imprime grafico de frecuencias de keywords
#dist.plot(10)
#print ('Keywords de la HV : ', counts.most_common(20))

#--------------------------------------

test_job = cleanDoc(job)
#print (test_job)
counts = Counter(test_job)

#dist_job = FreqDist(counts)
#imprime grafico de frecuencias de keywords
#dist_job.plot(10)
#print ('Keywords de la oferta : ', counts.most_common(20))

inter = set(test_hv) & set(test_job)
#inter = hv & job
#print ('Intersección de keywords entre oferta y HV ', inter)
# cantidad de palabras en comun
#Aqui faltaría analizar si una keyword se repite mas de una vez deberia de tener un bonus, tanto en la hv como en la oferta
#print ('Cantidad de palabras comunes', len(inter))

#https://stackoverflow.com/questions/8897593/similarity-between-two-text-documents
# otros metodos a probar para buscar eficiencia https://www.linkedin.com/pulse/measuring-text-similarity-python-ravi-shankar
vectorizer = TfidfVectorizer()
def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    puntaje = ((tfidf * tfidf.T).A)[0,1]
    # [0,1] is the positions in the matrix for the similarity since two text inputs will create a 2x2 symmetrical matrix
    return puntaje

puntaje_hv = cosine_sim(hv, job)
puntaje_Kwds = len(inter)
#No se por que me sale error en la linea de codigo de abajo, que ya tiene el texto preprocesado
#print (cosine_sim(test_hv, test_job))
#Prueba de que funciona
#print (cosine_sim('a little bird', 'a big dog barks'))

final = puntaje_hv*100 + puntaje_Kwds
print ('Puntaje Total : {:.2f}% '.format(final))

def exportPDF():
    import fpdf
    #En cmd de anaconda seguir estos pasos:
    #git clone https://github.com/reingart/pyfpdf.git
    #cd pyfpdf
    #pip install fpdf.py

    pdf = fpdf.FPDF(format='letter')
    pdf.add_page()
    #Aqui debe de ir nuestro logo y lema o algo asi
    pdf.image("logo.png", x=10, y=8, w=23)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resumen Hoja de Vida!", ln=1, align="C")
    pdf.cell(200, 10,"Hecho por Yob", 0, 1, 'C')
    pdf.cell(0, 20,"Tu porcentaje de afinidad con este empleo es de {:.2f}%".format(final), 0, 1,)
    y = 50
    w = 10
    #descomentar para probar NOT
    #cont = cont+500
    if cont>700:
        pdf.image("not.png", x=10, y=y, w=w)
        pdf.cell(90, 10, txt="Tu Hoja de vida tiene {} palabras".format(cont), ln=1, align="C")
        pdf.set_font("Arial", size=8)
        pdf.cell(90, 10, txt="Las hojas de vida mas interesantes tiene menos de 700 palabras, trata de ser mas preciso con lo que quieres decir")
    else:
        pdf.image("ok.png", x=10, y=y, w=10)
        pdf.set_font("Arial", size=10)
        pdf.cell(80, 10, txt="Tu Hoja de vida tiene {} palabras".format(cont),ln=1, align="C")
        pdf.set_font("Arial", size=8)
        pdf.cell(90,10 ,txt="Bien hecho! Las hojas de vida mas interesantes tiene menos de 700 palabras")
        pdf.output("tutorial.pdf")
        fin = time.time()
        print ('Tiempo total de ejecución : {:.4f} segundos'.format(fin-inicio))