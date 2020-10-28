'''
Queries - Program for retrieving information from an inverted index.
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

import sys
import getopt
import re
from index import Index
import string
import math
import web
from web import form
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Definimos el buscador
searcher = None # Se inicializa en el main

# Ruta de las plantillas
render = web.template.render('templates/')

# Estructura de URLS
urls = (
  '/', 'index',
  '/results', 'results'
)

# Formulario para las consultas
query_form = form.Form(
    form.Textbox("query", description="Query"),
    validators = [
        form.Validator("A query must be specified", lambda i: i.query == "")
    ]
)

# Clases para el servicio web
class index:
    def GET(self):
        return render.index(query_form())
    
    def POST(self):
        f = query_form()
        if not f.validates():
            return render.index(query_form())
        else:
            input_query = f["query"].value
            return render.results(searcher.process_query(input_query))

class results:
    def GET(self):
        return render.results()

# Funciones y clases para resolver el problema
def get_documents(filename):
    f = open(filename, "r")
    docs = { }
    for line in f.readlines():
        aux = re.split(r"(?<=\d)\D", line, maxsplit = 1)
        id_doc = aux[0]
        doc_text = aux[1]
        docs[id_doc] = doc_text
    f.close()
    return docs

def show_results(results, results_to_show = None):
    # Validaciones
    if len(results) < 1:
        print("No results found")
        return
    if results_to_show != None:
        if results_to_show < 1:
            results_to_show = len(results)
    else:
        results_to_show = len(results)
    # Mostramos los resultados
    print("Number of results found: " + str(len(results)))
    print("Showing " + str(results_to_show) + " results.")
    results_shown = 0
    for id_doc in results:
        if results_shown < results_to_show:
            print("ID Document: " + str(id_doc))
            results_shown += 1
        else:
            return

class Searcher:
    def __init__(self, index):
        self.index = index

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

    def __get_id_docs_for_terms__(terms, index):
        # Devuelve el id de los documentos que contienen los terminos
        id_docs = set()
        for t in terms:
            for id in index.get_post_list(t).keys():
                id_docs.add(id)
        return id_docs

    def __get_tf__(id_doc, term, index):
        try:
            return index.get_post_list(term)[id_doc]
        except KeyError:
            return 0

    def __cosine_similarity__(id_doc, bag, index):
        dot_product = 0
        aux_doc = 0
        aux_bag = 0
        for t in bag:
            # Document
            tf = __get_tf__(id_doc, t, index)
            idf = index.get_idf(t)
            # Bag
            tf_bag = bag[t] / sum(bag.values())
            # tf * idf
            tfidf_doc = idf * tf
            tfidf_bag = idf * tf_bag
            # Dot product
            dot_product += (tfidf_doc) * (tfidf_bag)
            # Para luego calcular la magnitud
            aux_doc += math.pow(tfidf_doc, 2)
            aux_bag += math.pow(tfidf_bag, 2)
        # Magnitudes
        magnitude_doc = math.sqrt(aux_doc)
        magnitude_bag = math.sqrt(aux_bag)
        return dot_product / (magnitude_doc * magnitude_bag)

    def __sort_by_score__(id_docs, bag, index):
        # Devuelve los id de los documentos ordenados por puntuacion
        score = { }
        for id_doc in id_docs:
            score[id_doc] = cosine_similarity(id_doc, bag, index)
        return sorted(score, key=score.get, reverse=True)

    def process_query(self, query):
        # Obtenemos la bolsa de terminos de la query
        bag = __string_to_bag_of_words__(query) 

        # Obtenemos el id de los documentos que contienen los terminos
        id_docs = __get_id_docs_for_terms__(bag.keys(), self.index)

        # Obtenemos el id de los documentos ordenados por puntuacion
        id_docs_sorted = __sort_by_score__(id_docs, bag, self.index)

        # Devolvemos los resultados
        return id_docs_sorted


def showHelp():
    print("Queries  Copyright (C) 2020  Hugo Fonseca Diaz")
    print("This program comes with ABSOLUTELY NO WARRANTY;")
    print("This is free software, and you are welcome to redistribute it")
    print("under certain conditions;")

    print("\nOverview:")
    print("Normally Queries is invoked like this:")
    print("\tqueries.py -q QUERY")
    print("\nCommand-Line Options:")
    print("The full format for invoking Queries is:")
    print("\tqueries.py OPTIONS")
    print("\tqueries.py -q QUERY")
    print("\n'-h'\n'--help'\n\tShow help")
    print("\n'-q'\n'--query'\n\tThe query")

def main(argv):
    # Creamos el fichero invertido
    index = Index()

    # Extraemos los documentos
    documents = get_documents("cran-1400.txt")

    # Rellenamos el indice
    for id_doc in documents.keys():
        index.load_document(id_doc, documents[id_doc])

    # Creamos el buscador
    searcher = Searcher(index)


if __name__ == "__main__":
    main(sys.argv[1:])

