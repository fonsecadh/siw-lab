'''
Crawler - Basic crawler for downloading HTML files from given URLs.
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
import requests
import time
from bs4 import BeautifulSoup
import urlparse
import codecs

class Crawler:
    def __init__(self, max_downloads, seconds):
        self.max_downloads = max_downloads
        self.seconds = seconds
        self.visited_urls = [ ]

    def procesar(self, file):
        txt = open(file, "r")
        for r in txt:
            self.crawl(r.rstrip("\n"))
        txt.close()

    def crawl(self, url):
        # Si llegamos al limite de descargas
        if self.max_downloads == 0:
            return
        # Si no hemos visitado la pagina
        if url in self.visited_urls:
            return
        # Si podemos seguir descargando
        html = self.descargar(url)
        # Comprobamos que es un HTML
        if html == "":
            return
        # Actualizamos el numero de descargas restantes
        self.max_downloads -= 1
        self.visited_urls.append(str(url))
        print(self.visited_urls)
        # Dormimos el programa
        time.sleep(self.seconds)
        # Llamamos a la libreria BeautifulSoup
        soup = BeautifulSoup(html, features="html.parser")
        # Creamos el fichero HTML
        self.guardar_html(soup, html)
        # Enseñamos informacion adicional
        if self.max_downloads > 0:
            print("Files to be downloaded: " + str(self.max_downloads))
        # Procesamos todos los links del documento HTML
        links = soup.find_all("a", href=True)
        # Procesamos los enlaces encontrados en el html
        for l in links:
            # Normalizamos el link
            link = self.normalizar_link(url, l["href"])
            # Hacemos crawl al link normalizado
            self.crawl(link)

    def descargar(self, url):
        request = requests.get(url)
        # Comprobar que sea un html        
        if "text/html" in request.headers["content-type"]:
            return request.text
        return ""

    def normalizar_link(self, url, link):
        if link.startswith("/") or link.startswith("#") or link.startswith("../"):
            # Usaremos la libreria urlparser
            return urlparse.urljoin(url, link)
        return link

    def guardar_html(self, soup, html):
        # Guardamos el documento html en un fichero
        with codecs.open(soup.title.string.replace("/", "-") + ".html", "w+", encoding="utf-8") as file:
            file.write(html)
            file.close()

def conseguir_urls(filename):
    file = open(filename, "r")
    lines = file.read().splitlines()
    urls = [ ]
    for line in lines:
        urls.append(line)
    file.close()
    return urls

def showHelp():
    print("Crawler  Copyright (C) 2020  Hugo Fonseca Diaz")
    print("This program comes with ABSOLUTELY NO WARRANTY;")
    print("This is free software, and you are welcome to redistribute it")
    print("under certain conditions;")

    print("\nOverview:")
    print("Normally 'Crawler' is invoked like this:")
    print("\tcrawler.py -i URLS_FILE -m MAX_FILES -s SECONDS_TO_WAIT")
    print("\nCommand-Line Options:")
    print("The full format for invoking 'Crawler' is:")
    print("\tcrawler.py OPTIONS")
    print("\tcrawler.py -i URLS_FILE -m MAX_FILES -s SECONDS_TO_WAIT")
    print("\n'-h'\n'--help'\n\tShow help")
    print("\n'-i'\n'--ifile'\n\tInput filename")
    print("\n'-m'\n'--maxfiles'\n\tMaximum number of files")
    print("\n'-s'\n'--seconds'\n\tSeconds to wait")


def main(argv):
    input_file = ""
    max_files = 0
    seconds = 0

    # Comprobamos que los argumentos introducidos sean validos
    try:
        opts, args = getopt.getopt(argv, "hi:m:s:",["help","ifile=","maxfiles=","secs="])
    except getopt.GetoptError:
        showHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            showHelp()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-m", "--maxfiles"):
            max_files = int(arg)
        elif opt in ("-s", "--secs"):
            seconds = int(arg)

    # Validamos argumentos
    if input_file == "" or max_files < 1 or seconds < 1:
        showHelp()
        sys.exit()

    # Mostramos informacion
    print("Input file: " + input_file)
    print("Max files to download: " + str(max_files))
    print("Time to wait between crawls: " + str(seconds))

    # Conseguimos las URL del fichero
    urls = conseguir_urls(input_file)
    # Instanciamos un objeto Crawler
    crawler = Crawler(max_files, seconds)
    # Procesamos las URL
    for url in urls:
        crawler.crawl(url)


if __name__ == "__main__":
    main(sys.argv[1:])


