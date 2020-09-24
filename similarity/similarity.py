from __future__ import division # Para resultados con decimales
import string

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
        return iter(self.values.viewitems())
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
    # TODO: Use NLTK
    return bag

def load_lines(filename):
    f = open(filename, "r")
    lines = { }
    # TODO: Process lines
    f.close()
    return lines

def main():
    texts = load_lines("cran-1400.txt")
    queries = load_lines("cran-queries.txt")
    for q in queries:
        print("Query: " + q)
        best_text = find_best_text(q, texts, coef_dice)
        print(" Dice coefficient: " + str(best_text))
        best_text = find_best_text(q, texts, coef_jaccard)
        print(" Jaccard coefficient: " + str(best_text))
        best_text = find_best_text(q, texts, coef_cosine)
        print(" Cosine coefficient: " + str(best_text))
        best_text = find_best_text(q, texts, coef_overlapping)
        print(" Overlapping coefficient: " + str(best_text) + "\n")






