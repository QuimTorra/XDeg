
from multiprocessing import Process
import logging
import argparse

from flask import Flask, render_template, request
from rdflib import Graph, Literal, Namespace, XSD, URIRef
from rdflib.namespace import FOAF, RDF

ECSDI = Namespace("http://www.owl-ontologies.com/ECSDI_XDeg.owl#")

gr = Graph()
bar_con = "Barcelona"
lon_con = "Londres"
rome_con = "Rome"
par_con = "Paris"


## BARCELONA ##

content = ECSDI['Destino_0']
gr.add((content, RDF.type, ECSDI.Destino))
gr.add((content, ECSDI.Nombre, Literal("barcelona", datatype=XSD.string)))

medio_trans_ciudad = ECSDI['Medio_De_Transporte_1']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Medio_De_Transporte))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('bus', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(50, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

medio_trans_ciudad = ECSDI['Medio_De_Transporte_2']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Medio_De_Transporte))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('plane', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(150, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

medio_trans_ciudad = ECSDI['Medio_De_Transporte_3']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Medio_De_Transporte))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('train', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(75, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

medio_trans_ciudad = ECSDI['Medio_De_Transporte_4']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Medio_De_Transporte))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('ferry', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(120, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))


## PARIS ##

content = ECSDI['Destino_1']
gr.add((content, RDF.type, ECSDI.Destino))
gr.add((content, ECSDI.Nombre, Literal("paris", datatype=XSD.string)))

medio_trans_ciudad = ECSDI['Medio_De_Transporte_5']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Medio_De_Transporte))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('plane', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(275, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

medio_trans_ciudad = ECSDI['Medio_De_Transporte_6']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Medio_De_Transporte))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('bus', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(70, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

medio_trans_ciudad = ECSDI['Medio_De_Transporte_7']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Medio_De_Transporte))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('train', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(40, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

## LONDON ##

content = ECSDI['Destino_2']
gr.add((content, RDF.type, ECSDI.Destino))
gr.add((content, ECSDI.Nombre, Literal("london", datatype=XSD.string)))

medio_trans_ciudad = ECSDI['Medio_De_Transporte_8']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Medio_De_Transporte))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('plane', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(240, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

medio_trans_ciudad = ECSDI['Medio_De_Transporte_9']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Medio_De_Transporte))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('ferry', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(120, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

## LONDON ##

content = ECSDI['Destino_3']
gr.add((content, RDF.type, ECSDI.Destino))
gr.add((content, ECSDI.Nombre, Literal("rome", datatype=XSD.string)))

medio_trans_ciudad = ECSDI['Medio_De_Transporte_10']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Medio_De_Transporte))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('plane', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(235, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))

medio_trans_ciudad = ECSDI['Medio_De_Transporte_11']
gr.add((medio_trans_ciudad, RDF.type, ECSDI.Medio_De_Transporte))
gr.add((medio_trans_ciudad, ECSDI.Nombre, Literal('train', datatype=XSD.string)))
gr.add((medio_trans_ciudad, ECSDI.Precio, Literal(85, datatype=XSD.integer)))
gr.add((medio_trans_ciudad, ECSDI.Pertenece_a, URIRef(content)))


#Recorregut per tota el Graf
for medio_t in gr.subjects(RDF.type, ECSDI.Medio_De_Transporte):
    print(gr.value(subject=medio_t, predicate=ECSDI.Pertenece_a),
          gr.value(subject=gr.value(subject=medio_t, predicate=ECSDI.Pertenece_a), predicate=ECSDI.Nombre),
          gr.value(subject=medio_t, predicate=ECSDI.Nombre),
          gr.value(subject=medio_t, predicate=ECSDI.Precio))
    

gr.serialize('Medio_Transporte_BD.rdf')

ontologyFile = open('./Medio_Transporte_BD.rdf')
gm = gr.parse(ontologyFile)

print('######')

for medio_t in gm.subjects(RDF.type, ECSDI.Medio_De_Transporte):
    print(gm.value(subject=medio_t, predicate=ECSDI.Pertenece_a),
          gm.value(subject=gr.value(subject=medio_t, predicate=ECSDI.Pertenece_a), predicate=ECSDI.Nombre),
          gm.value(subject=medio_t, predicate=ECSDI.Nombre),
          gm.value(subject=medio_t, predicate=ECSDI.Precio))