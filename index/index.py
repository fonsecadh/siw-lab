import string
import math

class Index:
    """
        Modela un fichero invertido.
    """
    def __init__(self, documents):
        # Cargamos los documentos al diccionario
        self.fill_index(documents)
        # Diccionario de terminos
        self.terms = { }
        # Numero de documentos
        self.n_documents = 0

    def __fill_index__(documents):
        pass

    def put(self, term, entry):
        # Añadimos la entrada al diccionario
        self.terms[term] = entry

    def contains_term(self, term):
        """ 
            Comprobamos que el termino este en el diccionario. Si no esta, se
            lanza una excepcion de tipo KeyError.
        """
        if term not in self.terms.keys():
            raise KeyError("El termino " + term + " no tiene entradas asociadas")

    def get(self, term):
        # Devuelve la entrada asociada a un termino dado
        self.contains_term(term)
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
    def __init__(self, term, n_documents, post_list, idf = 0):
        """
            Constructor de la IndexEntry.

            Params:
                term: termino asociado a la entrada.
                n_documents: numero de documentos en el diccionario.
                post_list: diccionario con identificadores de documentos donde 
                    aparece el termino y el valor TF del termino en cada uno de
                    ellos.
                idf: valor idf del termino.
        """
        self.term = term
        self.n_documents = n_documents
        self.post_list = post_list
        self.idf = idf

    def get_idf(self):
        pass


