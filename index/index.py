from __future__ import division
import string
import math

class Index:
    """
        Modela un fichero invertido.
    """
    def __init__(self):
        # Diccionario de terminos
        self.terms = { }
        # Numero de documentos
        self.n_documents = 0


