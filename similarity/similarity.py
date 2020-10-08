'''
Similarity - Program for finding similarities between texts.
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

from __future__ import division # Para resultados con decimales
import string
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class BagOfWords:
    def __init__(self, text=None, values=None):
        if text == "": # Recibe un diccionario
            self.values = values
        else: # Recibe un texto a convertir en diccionario
            self.values = string_to_bag_of_words(text)

    def __str__(self):
        # Devuelve un string representando al objeto
        return str(self.values)

    def __len__(self):
        # Devuelve el tamaño del diccionario
        return len(self.values)

    def __iter__(self):
        """
            Devuelve un iterador que retorna la clave y el valor
            de los elementos.
        """
        return iter(self.values.items())

    def intersection(self, other):
        # Intersecta dos bag-of-words
        intersected_bag = { x: self.values[x] for x in self.values if x in other.values }
        return BagOfWords(values=intersected_bag)

    def union(self, other):
        # Une dos bag-of-words
        unionized_bag = dict(other.values, **self.values)
        return BagOfWords(values=unionized_bag)

def string_to_bag_of_words(text):
    bag = { }
    # Eliminamos los simbolos de puntuacion (Excepto apostrofes)
    aux_punctuation = string.punctuation.replace("'", "")
    translated_text = text.translate(str.maketrans("", "", aux_punctuation))
    # Obtenemos los tokens
    tokens = nltk.word_tokenize(translated_text)
    # Procesamos los tokens
    lemmatizer = WordNetLemmatizer()
    for token in tokens:
        # Lematizamos el token
        token = lemmatizer.lemmatize(token.lower())
        if token not in stopwords.words('english'):
            # Si no es una stop word
            if token not in words:
                # Es la primera vez que aparece
                bag[token] = 1
            else:
                # Ya ha aparecido antes
                bag[token] += 1
    return bag

def load_lines(filename):
    f = open(filename, "r")
    lines = [ ]
    for line in f.readlines():
        # Solo guardamos el substring correspondiente al texto de la consulta
        lines.append(string_to_bag_of_words(line[5:]))
    f.close()
    return lines

def find_best_text(query, texts, coefficient):
    bag1 = BagOfWords(values = query) # Bag of words de la consulta
    best_result = 0 # Mejor resultado del coeficiente
    best_text = 0 # Numero del mejor texto
    text_number = 0 # Para llevar la cuenta de en que texto estamos
    for text in texts:
        text_number += 1
        bag2 = BagOfWords(values = text) # Bag of word del texto actual
        result = coefficient.execute(bag1, bag2) # Calculamos el coeficiente
        # Si el nuevo coeficiente es mayor que el actual mejor coeficiente
        if result > best_result: 
            # Actualizamos valores de las variables
            best_result = result
            best_text = counter
    # Devolvemos el numero del mejor texto
    return best_text
    

class Coefficient:
    def __init__(self, func=None):
        if func:
            # Reemplazamos la funcion
            self.execute = func

    # Strategy design pattern
    def execute(self, bag1, bag2):
        print("No coefficient function given")

# Strategy functions for calculating coefficients
def coef_dice(bag1, bag2):
    dividend = len(bag2.intersection(bag2))
    divisor = len(bag1) + len(bag2)
    return 2 * (dividend / divisor)

def coef_jaccard(bag1, bag2):
    dividend = len(bag1.intersection(bag2))
    divisor = len(bag1.union(bag2))
    return dividend / divisor

def coef_cosine(bag1, bag2):
    dividend = len(bag1.intersection(bag2))
    divisor = len(bag1) * len(bag2)
    return dividend / divisor

def coef_overlapping(bag1, bag2):
    dividend = len(bag1.intersection(bag2))
    divisor = min(len(bag1), len(bag2))
    return dividend / divisor

def main():
    texts = load_lines("cran-1400.txt")
    queries = load_lines("cran-queries.txt")
    for q in queries:
        print("Query: " + q)
        """ 
            Creamos objetos de la clase Coefficient con su 
            correspondiente funcion de coeficiente, siguiendo
            el patron de diseño estrategia.
        """
        best_text = find_best_text(q, texts, Coefficient(coef_dice))
        print(" Dice coefficient: " + str(best_text))
        best_text = find_best_text(q, texts, Coefficient(coef_jaccard))
        print(" Jaccard coefficient: " + str(best_text))
        best_text = find_best_text(q, texts, Coefficient(coef_cosine))
        print(" Cosine coefficient: " + str(best_text))
        best_text = find_best_text(q, texts, Coefficient(coef_overlapping))
        print(" Overlapping coefficient: " + str(best_text) + "\n")


if __name__ == "__main__":
    main()




