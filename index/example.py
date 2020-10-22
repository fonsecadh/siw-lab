import sys
import getopt
from index import Index

def showHelp():
    print("\nOverview:")
    print("Normally this program is invoked like this:")
    print("\texample.py -t TERM")
    print("\nCommand-Line Options:")
    print("The full format for invoking this program is:")
    print("\texample.py OPTIONS")
    print("\texample.py -t TERM")
    print("\n'-h'\n'--help'\n\tShow help")
    print("\n'-t'\n'--term'\n\tTerm to retrieve from index")

def main(argv):
    input_term = ""

    # Comprobamos que los argumentos introducidos sean validos
    try:
        opts, args = getopt.getopt(argv, "ht:",["help","term="])
    except getopt.GetoptError:
        showHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            showHelp()
            sys.exit()
        elif opt in ("-t", "--term"):
            input_term = arg

    # Validamos argumentos
    if input_term == "":
        showHelp()
        sys.exit()
    
    # Creamos el indice
    index = Index()

    # Extraemos los documentos
    documents = get_documents("cran-1400.txt")

    # Rellenamos el indice
    for id_doc in documents.keys():
        index.load_document(id_doc, documents[id_doc])

    # Mostramos el numero de terminos indexados
    print("Numero de terminos indexados: " + str(len(index.terms.keys())))

    try:
        # Mostramos el numero de documentos que contienen el termino dado
        print("Numero de documentos que contienen el termino " + str(input_term) + ": " 
                + len(index.get_post_list(str(input_term))))

        # Mostramos los documentos que contienen ese termino y su TF
        for id_doc in index.get_post_list(str(input_term)).keys():
            print("ID documento: " + str(id_doc))
            print("TF: " + str(index.get_post_list(str(input_term))[id_doc]))

        # Mostramos el idf del termino
        print("IDF termino: " + str(index.get_idf(str(input_term))))
    except KeyError as e:
        print(e)

if __name__ == "__main__":
    main(sys.argv[1:])

