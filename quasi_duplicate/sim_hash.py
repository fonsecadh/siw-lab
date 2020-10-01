import string
import json
import gzip
from heapq import heappush, heappop
import hashlib


def sim_hash(document, restrictiveness):
    # Sacamos los terminos del documento
    terms = string_to_bag_of_words(document).keys()
    # Definimos la cola de prioridad
    heap = [ ]
    # Añadimos los terminos a la cola
    # TODO

def string_to_bag_of_words(text):
    # TODO

def get_documents_from_compressed_json(filename):
    # TODO

def main():
    # TODO


if __name__ == "__main__":
    main()


