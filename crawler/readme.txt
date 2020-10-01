Hugo Fonseca Díaz (UO258318)

Requerimientos para la ejecución del programa:

    - Python 2.7
    - beautifulsoup4
    - urlparse4
    - requests

Modo de uso

"crawler.py" espera tres inputs del usuario, si no se introducen correctamente se mostrará la ayuda del programa. Esta ayuda también puede mostrarse mediante el comando:
    
    $ python2 crawler.py -h

A continuación se muestran dos ejemplos de uso para "crawler.py":

    - Ejemplo 1

        $ python2 crawler.py -i urls1.txt -m 4 -s 1

        Al introducir este comando se descargarán cuatro archivos, con esperas intermedias de un segundo cada una, utilizándose como semilla el fichero "urls1.txt".
        
        Los ficheros obtenidos son los siguientes:

            - "core - userspace foundation | suckless.org software that sucks less.html"
            - "dwm - dynamic window manager | suckless.org software that sucks less.html"
            - "software that sucks less | suckless.org software that sucks less.html"
            - "st - simple terminal | suckless.org software that sucks less.html"

    - Ejemplo 2

        $ python2 crawler.py -i urls2.txt -m 6 -s 2

        Este comando descargará seis archivos, con esperas intermedias de dos segundos cada una, utilizándose como semilla el fichero "urls2.txt".

        Los ficheros obtenidos son los siguientes:
        
            - "Change Log | qutebrowser.html"
            - "Contributing to qutebrowser | qutebrowser.html"
            - "Frequently asked questions | qutebrowser.html"
            - "Installing qutebrowser | qutebrowser.html"
            - "qutebrowser | qutebrowser.html"
            - "qutebrowser help | qutebrowser.html"

