'''
Simhash - Program for finding quasi-duplicates by means of a simhashing
algorithm.
Copyright (C) 2020  Hugo Fonseca Diaz
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import string
import json
import gzip
from heapq import heappush, heappop
import zlib
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def sim_hash(document, restrictiveness):
    # Creamos el set de terminos
    terms = string_to_bag_of_words(document).keys()
    # Validamos el valor de la restrictividad
    if restrictiveness > len(terms):
        print("La restrictividad es mayor que el numero de elementos del set")
        return
    # Definimos la cola de prioridad
    queue = [ ]
    # Añadimos los terminos a la cola
    for t in terms:
        heappush(queue, crc32_hash(t))
    # Inicializamos el simhash
    simhash = 0
    # Calculamos el simhash
    for x in range(0, restrictiveness):
        simhash += heappop(queue)
    return simhash

def string_to_bag_of_words(text):
    bag = { }
    # Eliminamos los simbolos de puntuacion (Excepto apostrofes)
    aux_punctuation = string.punctuation.replace("'", "")
    translated_text = str(text).translate(str.maketrans("", "", aux_punctuation))
    # Obtenemos los tokens
    tokens = nltk.word_tokenize(translated_text)
    # Procesamos los tokens
    lemmatizer = WordNetLemmatizer()
    for token in tokens:
        # Lematizamos el token
        token = lemmatizer.lemmatize(token.lower())
        if token not in stopwords.words('english'):
            # Si no es una stop word
            if token not in bag:
                # Es la primera vez que aparece
                bag[token] = 1
            else:
                # Ya ha aparecido antes
                bag[token] += 1
    return bag

def crc32_hash(term):
    return hex(zlib.crc32(term.encode("utf-8") & 0xffffffff))

def get_documents_from_txt(filename):
    f = open(filename, "r", errors = "ignore")
    lines_file = f.read().splitlines()
    aux = [ ]
    for line in lines_file:
        aux.append(line[4:])
    f.close()
    return aux

def get_documents_from_compressed_json(filename):
    # TODO
    pass

def show_results(quasi_duplicates):
    print("Simhash Algorithm.\n")
    print("Restrictiveness: " + str(restrictiveness))
    print("Results:")
    for d_simhash in quasi_duplicates:
        # Si hay documentos quasi-duplicados
        if len(quasi_duplicates[d_simhash]) > 1:
            print("\tSimhash " + str(d_simhash) + "\n")
            for d in quasi_duplicates[d_simhash]:
                # Mostramos los documentos quasi-duplicados
                print("\t\t- " + d)

def main():
    # Obtenemos los documentos
    docs = get_documents_from_txt("cran-1400.txt")
    # Asignamos el valor de restrictividad de nuestro algoritmo
    restrictiveness = 6
    # Obtenemos los documentos quasi-duplicados
    quasi_duplicates = { } # Diccionario de quasi-duplicados
    for d in docs:
        # Calculamos el simhash
        d_simhash = sim_hash(d, restrictiveness)
        if d_simhash not in quasi_duplicates.keys():
            """ 
                Añadimos una entrada al diccionario, la clave
                sera el simhash y el valor una lista en la que
                iremos introduciendo los documentos con ese valor
                de simhash.
            """
            quasi_duplicates.update({ d_simhash : [ ] })
        """
            Añadimos el documento a la lista de documentos que
            comparten ese simhash.
        """
        quasi_duplicates[d_simhash].append(d)
    # Mostramos los resultados
    show_results(quasi_duplicates)

if __name__ == "__main__":
    main()


