Hugo Fonseca Díaz (UO258318)

Requerimientos

    - Python 3.8
    - Bibliotecas nltk y web.py
    - Colección cran-1400.txt al mismo nivel que el script "queries.py"
    - Carpetas /static y /templates al mismo nivel que el script "queries.py"
    - Script "index.py" al mismo nivel que el script "queries.py"


Notas de uso

Para utilizar el script "queries.py", una vez que todos los requerimientos arriba descritos estén cumplidos, ejecutaremos el programa con:
    
    $ python queries.py

Esto desplegará un servicio web en "http://0.0.0.0:8080/". Una vez se entre a dicha URL se podrá observar una interfaz gráfica con una barra de búsqueda en la que se introducirá la consulta deseada. Al pulsar la tecla "Intro" deberán aparecer los identificadores de los documentos que satisfagan dicha consulta debajo de la barra de búsqueda. Estos identificadores son enlaces al contenido de los propios documentos, por lo que al clicar en ellos llevarán a una nueva ventana con el texto de su documento asociado.


Ejemplos de consultas

Se muestran los diez primeros documentos (en la aplicación se muestran todos) devueltos por cada consulta en orden de relevancia:

    - supersonic speed: I193, I226, I251, I80, I242, I814, I176, I1339, I60, I464

    - three-dimensional: I7, I700, I1100, I1220, I872, I1368, I182, I801, I916, I714

    - aerodynamic heating: I481, I342, I13, I978, I1147, I486, I95, I77, I981, I886

    - generalised-newtonian theory: I20, I820, I360, I503, I739, I1263, I930, I1140, I497, I179

    - nonequilibrium state of the boundary layer: I576, I396, I24, I1295, I541, I1189, I1210, I401, I625, I332

