'''
Index - Models an inverted index to be used by a search engine.
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
import math
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class Index:
    """
        Modela un fichero invertido.
    """
    def __init__(self):
        # Diccionario de terminos
        self.terms = { }
        # Numero de documentos
        self.n_documents = 0

    def load_document(self, id_doc, document):
        # Carga los terminos de un documento al diccionario
        self.n_documents += 1
        # Creamos la bag of words
        bag = self.__string_to_bag_of_words__(document)
        for t in bag.keys():
            if t not in self.terms.keys():
                # El termino no esta en el diccionario
                post_list = { }
                post_list[id_doc] = bag[t] # ID del documento y el TF asociado
                self.put(IndexEntry(t, post_list)) # Insertamos la entrada
            else:
                # El termino ya esta en el diccionario
                self.update_post_list(t, id_doc, bag[t])

    def put(self, term, entry):
        # Añadimos la entrada al diccionario
        self.terms[term] = entry

    def update_post_list(self, term, id_doc, tf):
        # Actualiza la post_list de la entrada asociada al termino
        self.terms[term].update_post_list(id_doc, tf)

    def get_post_list(self, term):
        # Devuelve la post-list de la entrada asociada al termino
        return self.get(term).get_post_list()

    def get_idf(self, term):
        # Devuelve el idf de un termino
        return self.get(term).get_idf(self.n_documents)

    def __contains_term__(self, term):
        """ 
            Comprobamos que el termino este en el diccionario. Si no esta, se
            lanza una excepcion de tipo KeyError.
        """
        if term not in self.terms.keys():
            raise KeyError("El termino " + term + " no tiene entradas asociadas")

    def get(self, term):
        # Devuelve la entrada asociada a un termino dado
        self.__contains_term__(term) # Validamos el input
        return self.terms[term]

    def __string_to_bag_of_words__(text):
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


class IndexEntry:
    """
        Modela una entrada del fichero invertido.
    """
    def __init__(self, term, post_list):
        """
            Constructor de la IndexEntry.

            Params:
                term: termino asociado a la entrada.
                post_list: diccionario con identificadores de documentos donde 
                    aparece el termino y el valor TF del termino en cada uno de
                    ellos.
        """
        self.term = term
        self.post_list = post_list

    def get_idf(self, n_documents):
        # Evitamos una division por cero
        n_doc_with_term = len(self.post_list) + 1
        # Calculamos el idf
        return math.log10(n_documents / n_doc_with_term)

    def get_post_list(self):
        return self.post_list

    def update_post_list(self, id_doc, tf):
        self.post_list[id_doc] = tf

