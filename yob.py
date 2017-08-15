import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

#importar el texto
hv = open('resume.txt')

#1 Contar las palabras de la hoja de vida
wordcount = Counter(hv.read().split())
cont = 0
for item in wordcount.items():
    #imprime cada palabra y su frecuencia
    #print("{}\t{}".format(*item))
    cont += item[1]
print('Total palabras ',cont)