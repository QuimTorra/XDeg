
from multiprocessing import Process
import logging
import argparse

from flask import Flask, render_template, request
from rdflib import Graph, Literal, Namespace, XSD, URIRef
from rdflib.namespace import FOAF, RDF
import sys
sys.path.insert(1, '../Agentes')
from AgentUtil.OntoNamespaces import ECSDI


gr = Graph()
bar_con = "Barcelona"
lon_con = "Londres"
rome_con = "Rome"
par_con = "Paris"


## BARCELONA ##

content = ECSDI['Destino_0']
gr.add((content, RDF.type, ECSDI.Destino))
gr.add((content, ECSDI.Nombre, Literal("barcelona", datatype=XSD.string)))

medio_trans_ciudad = ECSDI['Alojamiento_1']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Alojamiento))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('hotel', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(100, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Estrellas, Literal(4, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

medio_trans_ciudad = ECSDI['Alojamiento_2']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Alojamiento))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('apartamento', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(80, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Estrellas, Literal(4, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

medio_trans_ciudad = ECSDI['Alojamiento_3']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Alojamiento))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('camping', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(66, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Estrellas, Literal(1, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

medio_trans_ciudad = ECSDI['Alojamiento_4']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Alojamiento))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('apartamento', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(95, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Estrellas, Literal(5, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))


## PARIS ##

content = ECSDI['Destino_1']
gr.add((content, RDF.type, ECSDI.Destino))
gr.add((content, ECSDI.Nombre, Literal("paris", datatype=XSD.string)))

medio_trans_ciudad = ECSDI['Alojamiento_5']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Alojamiento))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('hotel', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(160, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Estrellas, Literal(4, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

medio_trans_ciudad = ECSDI['Alojamiento_6']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Alojamiento))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('apartamento', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(90, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Estrellas, Literal(5, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

medio_trans_ciudad = ECSDI['Alojamiento_7']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Alojamiento))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('camping', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(70, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Estrellas, Literal(3, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

## LONDON ##

content = ECSDI['Destino_2']
gr.add((content, RDF.type, ECSDI.Destino))
gr.add((content, ECSDI.Nombre, Literal("london", datatype=XSD.string)))

medio_trans_ciudad = ECSDI['Alojamiento_8']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Alojamiento))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('hotel', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(110, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Estrellas, Literal(5, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

medio_trans_ciudad = ECSDI['Alojamiento_9']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Alojamiento))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('deg', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(250, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Estrellas, Literal(5, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

## ROME ##

content = ECSDI['Destino_3']
gr.add((content, RDF.type, ECSDI.Destino))
gr.add((content, ECSDI.Nombre, Literal("rome", datatype=XSD.string)))

medio_trans_ciudad = ECSDI['Alojamiento_10']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Alojamiento))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('hotel', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(70, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Estrellas, Literal(3, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

medio_trans_ciudad = ECSDI['Alojamiento_11']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Alojamiento))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('casa rural', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(120, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Estrellas, Literal(4, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

medio_trans_ciudad = ECSDI['Alojamiento_12']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Alojamiento))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('camping', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(50, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Estrellas, Literal(2, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

medio_trans_ciudad = ECSDI['Alojamiento_13']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Alojamiento))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('deg', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(240, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Estrellas, Literal(5, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))


#Recorregut per tota el Graf
for medio_t in gr.subjects(RDF.type, ECSDI.Alojamiento):
    print(gr.value(subject=medio_t, predicate=ECSDI.Pertenece_a),
          gr.value(subject=gr.value(subject=medio_t, predicate=ECSDI.Pertenece_a), predicate=ECSDI.Nombre),
          gr.value(subject=medio_t, predicate=ECSDI.Nombre),
          gr.value(subject=medio_t, predicate=ECSDI.Precio))
    

gr.serialize('Alojamiento_BD.rdf')

ontologyFile = open('./Alojamiento_BD.rdf')
gm = Graph()
gm = gm.parse(ontologyFile)

print('######')

for medio_t in gm.subjects(RDF.type, ECSDI.Alojamiento):
    print(gm.value(subject=medio_t, predicate=ECSDI.Pertenece_a),
          gm.value(subject=gm.value(subject=medio_t, predicate=ECSDI.Pertenece_a), predicate=ECSDI.Nombre),
          gm.value(subject=medio_t, predicate=ECSDI.Nombre),
          gm.value(subject=medio_t, predicate=ECSDI.Precio))