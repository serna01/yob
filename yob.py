import re
from nltk.corpus import stopwords
from nltk.corpus.reader.plaintext import WordPunctTokenizer
#from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import time

inicio = time.time()

#funciones soporte:
def cleanDoc(doc):
    stopset = set(stopwords.words('spanish'))
    #stemmer = PorterStemmer()
    stemmer = SnowballStemmer('spanish')
    tokens = WordPunctTokenizer().tokenize(doc)
    clean = [token.lower() for token in tokens if token.lower() not in stopset and len(token) > 2]
    final = [stemmer.stem(word) for word in clean]
    return final

def cosine_sim(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([text1, text2])
    puntaje = ((tfidf * tfidf.T).A)[0,1]
    # [0,1] is the positions in the matrix for the similarity since two text inputs will create a 2x2 symmetrical matrix
    return puntaje

def getIntersecTopN(inicial,final,test_hv,test_job):
    #saca el numero de palabras comunes a los 2 textos en el intervalo determinado
    counts_hv = Counter(test_hv)
    counts_job = Counter(test_job)
    mchI = counts_hv.most_common(inicial)
    mcjI = counts_job.most_common(inicial)
    mchF = counts_hv.most_common(final)
    mcjF = counts_job.most_common(final)

    mch=set(mchF)-set(mchI)
    mcj=set(mcjF)-set(mcjI)

    toph=[]
    topj=[]
    for i in mch:
        toph.append(i[0])
    for i in mcj:
        topj.append(i[0])
    interTop=set(toph) & set(topj)
    return len(interTop)

#funciones principales:
def contarPalabras(wordcount):
    cont=0
    for i in wordcount.items():
        cont+=i[1]
    return cont

def extraerDatosGenerales(hv):
    wordcount = Counter(hv.split())
    cont = 0
    email = []
    for item in wordcount.items():
        cont += item[1]
        # Extraer correo electronico
        if '@' in item[0]:
            email.append(item[0])
    tel = []
    for i, item in enumerate(
            re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',
                       hv)):
        tel.append(item)
    return email,tel

def calcularCalificacion(hv,job):
    #comparación de textos planos:
    puntaje_hv = cosine_sim(hv, job)*100
    
    #comparación de intersección de keywords:
    test_hv = cleanDoc(hv)
    test_job = cleanDoc(job)

    #Dar 0.5 puntos por cada intersección neta:
    puntaje_hv += getIntersecTopN(0, 1000, test_hv, test_job)*0.5

    #dar 1 punto por cada palabra comun en el rango 30 a 70 de cada texto:
    puntaje_hv+=getIntersecTopN(30,70,test_hv,test_job)

    #dar 1.5 puntos por cada palabra comun en el rango 10 a 30 de cada texto:
    puntaje_hv += getIntersecTopN(10, 30, test_hv, test_job)*1.5

    # dar 2 puntos por cada palabra comun en los top 10 de cada texto:
    puntaje_hv += getIntersecTopN(0, 10, test_hv, test_job)*2
    
    # limitar el puntaje al 100%:
    if (puntaje_hv>100):
        puntaje_hv=100

    return puntaje_hv

def palabrasComunesNoStemmer(doc,n):
    stopset = set(stopwords.words('spanish'))
    tokens = WordPunctTokenizer().tokenize(doc)
    clean = [token.lower() for token in tokens if token.lower() not in stopset and len(token) > 2]
    wordcount = Counter(clean)
    return wordcount.most_common(n)

def palabrasComunesStemmer(texto,n):
    cleanText=cleanDoc(texto)
    wordcount = Counter(cleanText)
    most_common=wordcount.most_common(n)
    stopset = set(stopwords.words('spanish'))
    tokens = WordPunctTokenizer().tokenize(texto)
    cleanNoStop = [token.lower() for token in tokens if token.lower() not in stopset and len(token) > 2]
    final={}
    for i in most_common:
        for j in cleanNoStop:
            if i[0] in j[:len(i[0])]:
                final[j]=i[1]
                break
    return final


def yobFunct(hv,job):
    calificacion=0

    #1: contar # de palabras de la HV:
    wordcount = Counter(hv.split())
    numPalabras=contarPalabras(wordcount)
    if numPalabras>400: #Idea: restar calificación en un 10% si la HV está muy larga
        calificacion-=10

    #2: extraer datos generales de la HV:
    [email,tel]=extraerDatosGenerales(hv)
    if email==[] or tel==[]: #Idea: restar calificación en un 10% si la HV no reconoce o el telefono o el correo
        calificacion -= 10

    #3: Entregar un puntaje de acuerdo a los parámetros de similitud del texto:
    calificacion=calcularCalificacion(hv,job)

    #print('CALIFICACIÓN DE AFINIDAD:',calificacion)
    #PUEDE SER!!! 4: Entregar N palabras más comunes de cada texto sin stopwords pero sin aplicar stemmer para hacer histograma en HTML:
    n=15
    #most_common_HV=palabrasComunesNoStemmer(hv,n)
    #most_common_Job=palabrasComunesNoStemmer(job,n)
    # Tambien puede ser que se aplique el stemmer y buscar la "palabra completa", y poner como "palabras relacionadas con: ej. geología"
    most_common_HV=palabrasComunesStemmer(hv,n)
    most_common_Job = palabrasComunesStemmer(job,n)
    #print('persona',most_common_HV)
    #print('trabajo',most_common_Job)
    #5: exportar informe en PDF
    #exportPDF()
    fin = time.time()
    #print('TIEMPO DE EJECUCIÓN:',fin-inicio)
    return(calificacion,most_common_HV,most_common_Job,numPalabrass)

if __name__ == '__main__':
    #0: importar HV y descripción del empleo:
    hv = open('resume_es.txt', encoding="utf8")
    job = open('empleo_ing_geol.txt', encoding="ANSI")
    hv = hv.read()
    job = job.read()
    result=yobFunct(hv,job)
    print(result[0],result[1],result[2])


