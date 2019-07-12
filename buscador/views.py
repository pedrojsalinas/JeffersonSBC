from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import *
import spacy
import es_core_news_sm
import rdflib
from rdflib.serializer import Serializer
from collections import OrderedDict
import itertools

class InicioView(TemplateView):
    plantilla = 'buscador/index.html'
    formulario = BuscadorForm()

    def get(self, request):
        args = {"formulario": self.formulario}
        return render(request, self.plantilla, args)

    def post(self, request):
        formulario = BuscadorForm(request.POST)
        if formulario.is_valid():
            text = formulario.cleaned_data['query']
            token = Semantico()
            datos = token.limpiezaDatos(text)
            args = {"datos": datos, "formulario": self.formulario}
        return render(request, self.plantilla, args)


class Detalles(TemplateView):
    plantilla = 'buscador/detalles.html'
    def get(self, request, id):
        response = id
        uri = 'http://data.utpl.edu.ec/casoav/resources/'
        uri = uri+response
        token = Semantico()
        datos = token.obtenerRecursos(uri)
        args = {"datos": datos}
        return render(request, self.plantilla,args)

class Semantico():
    g = rdflib.Graph()
    g.parse("datos.rdf")
    def obtenerRecursos(self, uri):
        datos = []
        consulta = """SELECT ?p ?o
                        WHERE
                        {
                            <%s> ?p  ?o
                        }""" % (uri)

        datos = []
        for row in self.g.query(consulta):
            recursos = []
            p = row.p.split("/")
            o = row.o.split("/")
            p = p[len(p)-1]
            o = o[len(o)-1]
            recursos.append(row.p)
            recursos.append(p)
            recursos.append(row.o)
            recursos.append(o)
            datos.append(recursos)
        return datos

    def limpiezaDatos(self, text):
        nlp = es_core_news_sm.load()
        text = nlp(text)
        tokenized_sentences = [sentence.text for sentence in text.sents]
  
        datos = []

        for sentence in tokenized_sentences:
            for entity in nlp(sentence).ents:
                consulta = 'SELECT ?s ?p ?o  WHERE { ?s ?p ?o .FILTER regex(str(?s), "%s") .}' % (
                    entity.text)
                for row in self.g.query(consulta):
                    tripleta = []
                    sujeto = row.s                    
                    predicado = row.p.split("/")
                    objeto = row.o.split("/")
                    objetoUri = row.o
                    predicado = predicado[len(predicado)-1]
                    objeto = objeto[len(objeto)-1]
                    # if '$' in objetoUri:
                    #     objetoUri = ''
                    tripleta.append(entity.text)
                    tripleta.append(sujeto)
                    tripleta.append(predicado)
                    tripleta.append(objeto)
                    tripleta.append(objetoUri)
                    datos.append(tripleta)
        datos = OrderedDict((tuple(x), x) for x in datos).values()
        lista = []
        for i in datos:
            lista.append(i)
        return lista
