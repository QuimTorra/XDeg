
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

actividades_ciudad = ECSDI['Actividad_1']
gr.add((actividades_ciudad, RDF.type, ECSDI.Actividad))
gr.add((actividades_ciudad, ECSDI.Nombre, Literal('Visitar Sagrada Familia', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Tipo, Literal('Cultural', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Interior, Literal('Interior', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Pertenece_a, URIRef(content)))

actividades_ciudad = ECSDI['Actividad_2']
gr.add((actividades_ciudad, RDF.type, ECSDI.Actividad))
gr.add((actividades_ciudad, ECSDI.Nombre, Literal('Concerts Palau de la Musica', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Tipo, Literal('Cultural', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Interior, Literal('Interior', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Pertenece_a, URIRef(content)))

actividades_ciudad = ECSDI['Actividad_3']
gr.add((actividades_ciudad, RDF.type, ECSDI.Actividad))
gr.add((actividades_ciudad, ECSDI.Nombre, Literal('ScapeRoom', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Tipo, Literal('Ludica', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Interior, Literal('Interior', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Pertenece_a, URIRef(content)))

actividades_ciudad = ECSDI['Actividad_4']
gr.add((actividades_ciudad, RDF.type, ECSDI.Actividad))
gr.add((actividades_ciudad, ECSDI.Nombre, Literal('Ball de Festa Major', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Tipo, Literal('Festiva', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Interior, Literal('Exterior', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Pertenece_a, URIRef(content)))

actividades_ciudad = ECSDI['Actividad_5']
gr.add((actividades_ciudad, RDF.type, ECSDI.Actividad))
gr.add((actividades_ciudad, ECSDI.Nombre, Literal('Tibidabo', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Tipo, Literal('Ludica', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Interior, Literal('Exterior', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Pertenece_a, URIRef(content)))

## PARIS ##

content = ECSDI['Destino_1']
gr.add((content, RDF.type, ECSDI.Destino))
gr.add((content, ECSDI.Nombre, Literal("paris", datatype=XSD.string)))

actividades_ciudad = ECSDI['Actividad_6']
gr.add((actividades_ciudad, RDF.type, ECSDI.Actividad))
gr.add((actividades_ciudad, ECSDI.Nombre, Literal('Comer Baggetes y Cuasons', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Tipo, Literal('Cultural', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Interior, Literal('Interior', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Pertenece_a, URIRef(content)))

actividades_ciudad = ECSDI['Actividad_7']
gr.add((actividades_ciudad, RDF.type, ECSDI.Actividad))
gr.add((actividades_ciudad, ECSDI.Nombre, Literal('Museo Louvre', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Tipo, Literal('Cultural', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Interior, Literal('Interior', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Pertenece_a, URIRef(content)))

actividades_ciudad = ECSDI['Actividad_8']
gr.add((actividades_ciudad, RDF.type, ECSDI.Actividad))
gr.add((actividades_ciudad, ECSDI.Nombre, Literal('DisneyLand', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Tipo, Literal('Ludica', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Interior, Literal('Exterior', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Pertenece_a, URIRef(content)))

actividades_ciudad = ECSDI['Actividad_9']
gr.add((actividades_ciudad, RDF.type, ECSDI.Actividad))
gr.add((actividades_ciudad, ECSDI.Nombre, Literal('Visitar Torre Eiffel', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Tipo, Literal('Cultural', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Interior, Literal('Exterior', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Pertenece_a, URIRef(content)))

## LONDON ##

content = ECSDI['Destino_2']
gr.add((content, RDF.type, ECSDI.Destino))
gr.add((content, ECSDI.Nombre, Literal("london", datatype=XSD.string)))

actividades_ciudad = ECSDI['Actividad_10']
gr.add((actividades_ciudad, RDF.type, ECSDI.Actividad))
gr.add((actividades_ciudad, ECSDI.Nombre, Literal('The London Eye', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Tipo, Literal('Cultural', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Interior, Literal('Exterior', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Pertenece_a, URIRef(content)))

actividades_ciudad = ECSDI['Actividad_11']
gr.add((actividades_ciudad, RDF.type, ECSDI.Actividad))
gr.add((actividades_ciudad, ECSDI.Nombre, Literal('Visitar Big Ben', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Tipo, Literal('Cultural', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Interior, Literal('Exterior', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Pertenece_a, URIRef(content)))

actividades_ciudad = ECSDI['Actividad_12']
gr.add((actividades_ciudad, RDF.type, ECSDI.Actividad))
gr.add((actividades_ciudad, ECSDI.Nombre, Literal('Ice Skating', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Tipo, Literal('Ludica', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Interior, Literal('Interior', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Pertenece_a, URIRef(content)))

actividades_ciudad = ECSDI['Actividad_13']
gr.add((actividades_ciudad, RDF.type, ECSDI.Actividad))
gr.add((actividades_ciudad, ECSDI.Nombre, Literal('13th Century Dance Hall', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Tipo, Literal('Festiva', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Interior, Literal('Interior', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Pertenece_a, URIRef(content)))

## ROME ##

content = ECSDI['Destino_3']
gr.add((content, RDF.type, ECSDI.Destino))
gr.add((content, ECSDI.Nombre, Literal("rome", datatype=XSD.string)))

actividades_ciudad = ECSDI['Actividad_14']
gr.add((actividades_ciudad, RDF.type, ECSDI.Actividad))
gr.add((actividades_ciudad, ECSDI.Nombre, Literal('Visitar Coliseo', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Tipo, Literal('Cultural', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Interior, Literal('Exterior', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Pertenece_a, URIRef(content)))

actividades_ciudad = ECSDI['Actividad_15']
gr.add((actividades_ciudad, RDF.type, ECSDI.Actividad))
gr.add((actividades_ciudad, ECSDI.Nombre, Literal('Visitar Vaticano', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Tipo, Literal('Cultural', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Interior, Literal('Interior', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Pertenece_a, URIRef(content)))

actividades_ciudad = ECSDI['Actividad_16']
gr.add((actividades_ciudad, RDF.type, ECSDI.Actividad))
gr.add((actividades_ciudad, ECSDI.Nombre, Literal('Lucha en el Coliseo', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Tipo, Literal('Ludica', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Interior, Literal('Exterior', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Pertenece_a, URIRef(content)))

actividades_ciudad = ECSDI['Actividad_17']
gr.add((actividades_ciudad, RDF.type, ECSDI.Actividad))
gr.add((actividades_ciudad, ECSDI.Nombre, Literal('Construye tu propio Coliseo (miniatura) con degref!', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Tipo, Literal('Festiva', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Interior, Literal('Interior', datatype=XSD.string)))
gr.add((actividades_ciudad, ECSDI.Pertenece_a, URIRef(content)))

#Recorregut per tota el Graf
for act_c in gr.subjects(RDF.type, ECSDI.Actividad):
    print(gr.value(subject=act_c, predicate=ECSDI.Pertenece_a),
          gr.value(subject=gr.value(subject=act_c, predicate=ECSDI.Pertenece_a), predicate=ECSDI.Nombre),
          gr.value(subject=act_c, predicate=ECSDI.Tipo),
          gr.value(subject=act_c, predicate=ECSDI.Interior))
    

gr.serialize('Activity_BD.rdf')

ontologyFile = open('./Activity_BD.rdf')
gm = Graph()
gm = gm.parse(ontologyFile)

print('######')

for act_c in gm.subjects(RDF.type, ECSDI.Actividad):
    print(gm.value(subject=act_c, predicate=ECSDI.Pertenece_a),
          gm.value(subject=gm.value(subject=act_c, predicate=ECSDI.Pertenece_a), predicate=ECSDI.Nombre),
          gm.value(subject=act_c, predicate=ECSDI.Tipo),
          gm.value(subject=act_c, predicate=ECSDI.Interior))