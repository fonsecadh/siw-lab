import sys
import requests
import time
from bs4 import BeautifulSoup
from urlparse import urljoin

class Crawler:
    def __init__(self, max_downloads, seconds):
        self.max_downloads = max_downloads
        self.seconds = seconds

    def procesar(self, file):
        txt = open(file, "r")
        for r in txt:
            self.crawl(r.rstrip("\n"))
        txt.close()

    def crawl(self, url):
        # Si llegamos al limite de descargas
        if self.max_downloads == 0:
            return
        # Si podemos seguir descargando
        html = requests.get(url)
        --self.max_downloads
        time.sleep(seconds)
        # Llamamos a la librería BeautifulSoup
        soup = BeautifulSoup(html.text, features="html.parser")
        links = soup.find_all("a", href=True)
        # Procesamos los enlaces encontrados en el html
        for l in links:
            # Normalizamos el link
            l = normalizar_link(url, l)
            # Hacemos crawl al link normalizado
            self.crawl(l)

    def normalizar_link(url, link):
        if link.startswith("/") or link.startswith("#"):
            # Usaremos la librería urlparser
            return urljoin(url, link)
        return link





