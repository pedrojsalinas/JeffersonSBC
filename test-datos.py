import spacy
import es_core_news_sm
import rdflib
from rdflib.serializer import Serializer
# mydataset
uri = 'http://data.utpl.edu.ec/casoav/resources/KoreaImplicadoJuicio'
g = rdflib.Graph()
# nombre del archivo
g.parse("datos.rdf")

consulta = """SELECT ?p ?o
                        WHERE
                        {
                            <%s> ?p  ?o
                        }""" % (uri)
datos = []

for row in g.query(consulta):
    recursos = []
    recursos.append(row.p)
    recursos.append(row.o)
    datos.append(recursos)

print(datos)
