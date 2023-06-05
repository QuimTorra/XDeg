__author__ = 'quimtorra'

from socket import gethostname
import socket
from flask import Flask, request, Response
from flask.json import jsonify
import json
import argparse
from rdflib import FOAF, RDF, Graph, Literal, Namespace, XSD
import requests
import logging
from requests import ConnectionError
from multiprocessing import Process
import string
import random

from AgentUtil.ACLMessages import get_message_properties
from AgentUtil.ACLMessages import build_message
from AGestorTransporte import GestorTransporte
from AgentUtil.ACL import ACL
from AgentUtil.Agent import Agent
from AgentUtil.DSO import DSO
from AgentUtil.ACLMessages import send_message
from AgentUtil.Logging import config_logger
from SimpleDirectoryAgent import DirectoryAgent
from AgentUtil.OntoNamespaces import ECSDI


# Definimos los parametros de la linea de comandos
parser = argparse.ArgumentParser()
parser.add_argument('--host', default='localhost', help="Host del agente")
parser.add_argument('--port', type=int,  help="Puerto de comunicacion del agente")
parser.add_argument('--dhost', help="Host del agente de directorio")
parser.add_argument('--dport', type=int, help="Puerto de comunicacion del agente de directorio")
parser.add_argument('--open', help="Define si el servidor est abierto al exterior o no", action='store_true',
                    default=False)
parser.add_argument('--verbose', help="Genera un log de la comunicacion del servidor web", action='store_true',
                        default=False)
parser.add_argument('--messages', nargs='+', default=[], help="mensajes a enviar")

# parsing de los parametros de la linea de comandos
args = parser.parse_args()

# Configuration stuff
if args.port is None:
    port = 9050
else:
    port = args.port

if args.open:
    hostname = '0.0.0.0'
    hostaddr = gethostname()
else:
    hostaddr = hostname = socket.gethostname()

print('DS Hostname =', hostaddr)

if args.dport is None:
    dport = 9000
else:
    dport = args.dport

if args.dhost is None:
    dhostname = socket.gethostname()
else:
    dhostname = args.dhost

app = Flask(__name__)

agn = Namespace("http://www.agentes.org#")

AgenciaTransporte = Agent('AgenciaTransporte',
                    agn.AgenciaTransporte,
                    'http://%s:%d/comm' % (hostaddr, port),
                    'http://%s:%d/Stop' % (hostaddr, port))

mss_cnt = 0

ontologyFile = open('../data/Medio_Transporte_BD.rdf')
fuente_Datos = Graph()
fuente_Datos = fuente_Datos.parse(ontologyFile)

#CHECKOUT DATABASE
# print('######')
# for medio_t in fuente_Datos.subjects(RDF.type, ECSDI.Medio_De_Transporte):
#     print(fuente_Datos.value(subject=medio_t, predicate=ECSDI.Pertenece_a),
#           fuente_Datos.value(subject=fuente_Datos.value(subject=medio_t, predicate=ECSDI.Pertenece_a), predicate=ECSDI.Nombre),
#           fuente_Datos.value(subject=medio_t, predicate=ECSDI.Nombre),
#           fuente_Datos.value(subject=medio_t, predicate=ECSDI.Precio))
# print('######')

def get_count():
    global mss_cnt
    if not mss_cnt:
        mss_cnt = 0
    mss_cnt += 1
    return mss_cnt

def register_message():
    """
    Envia un mensaje de registro al servicio de registro
    usando una performativa Request y una accion Register del
    servicio de directorio

    :param gmess:
    :return:
    """

    # logger.info('Nos registramos')
    print("Nos registramos")

    global mss_cnt

    gmess = Graph()

    # Construimos el mensaje de registro
    gmess.bind('foaf', FOAF)
    gmess.bind('dso', DSO)
    reg_obj = agn[AgenciaTransporte.name + '-Register']
    gmess.add((reg_obj, RDF.type, DSO.Register))
    gmess.add((reg_obj, DSO.Uri, AgenciaTransporte.uri))
    gmess.add((reg_obj, FOAF.name, Literal(AgenciaTransporte.name)))
    gmess.add((reg_obj, DSO.Address, Literal(AgenciaTransporte.address)))
    gmess.add((reg_obj, DSO.AgentType, DSO.AgenciaTransporte))

    # Lo metemos en un envoltorio FIPA-ACL y lo enviamos
    gr = send_message(
        build_message(gmess, perf=ACL.request,
                      sender=AgenciaTransporte.uri,
                      receiver=DirectoryAgent.uri,
                      content=reg_obj,
                      msgcnt=mss_cnt),
        DirectoryAgent.address)
    mss_cnt += 1

    return gr

@app.route("/")
def isAlive():
  text = 'Hi i\'m AExtTransporte o/, if you wanna travel go to <a href= /transport?coses=deg>here</a>'
  return text

@app.route("/transport")
def getTransport():
  # host:port/transport
  
  message = request.args['content']
  gm = Graph()
  gm.parse(data=message, format='xml')

  msgdic = get_message_properties(gm)
  content = msgdic['content']

  #accion (La peticion es valida)
  accion = gm.value(subject=content, predicate=RDF.type)
  if accion == ECSDI.Pedir_metodo_transporte:        
    destino = gm.value(subject=content, predicate=ECSDI.Destino)
    data_ini = gm.value(subject=content, predicate=ECSDI.Data_Ini)
    data_fi = gm.value(subject=content, predicate=ECSDI.Data_Fi)

    grespuesta = Graph()
    contentResult = ECSDI['Cerca_productes_' + str(get_count())]
    #OBTAIN FROM DATABASE
    for medio_t in fuente_Datos.subjects(RDF.type, ECSDI.Medio_De_Transporte):
        id_destino = fuente_Datos.value(subject=medio_t, predicate=ECSDI.Pertenece_a)

        #Metodo transporte hacia el destiono
        if fuente_Datos.value(subject=id_destino, predicate=ECSDI.Nombre) == destino:
            price_trans = fuente_Datos.value(subject=medio_t, predicate=ECSDI.Precio)
            name_trans = fuente_Datos.value(subject=medio_t, predicate=ECSDI.Nombre)

            medio_trans_ciudad = ECSDI['Medio_De_Transporte_'+ str(get_count())]
            grespuesta.add((medio_trans_ciudad, RDF.type, ECSDI.Medio_De_Transporte))
            grespuesta.add((medio_trans_ciudad, ECSDI.Nombre, Literal(name_trans, datatype=XSD.string)))
            grespuesta.add((medio_trans_ciudad, ECSDI.Precio, Literal(price_trans, datatype=XSD.integer)))
    
    print("#### RESULTADO QUERY ####")
    for medio_t in grespuesta.subjects(RDF.type, ECSDI.Medio_De_Transporte):
        print(destino,
            grespuesta.value(subject=medio_t, predicate=ECSDI.Nombre),
            grespuesta.value(subject=medio_t, predicate=ECSDI.Precio))

    gr = build_message(grespuesta,
                    ACL['inform'],
                    sender=AgenciaTransporte.uri,
                    content=Literal('OPTIONS AVAILABLE')).serialize(format='xml')
    
  else:  
    gr = build_message(Graph(),
                        ACL['inform'],
                        sender=AgenciaTransporte.uri,
                        content=Literal("NO OPTIONS AVAILABLE")).serialize(format='xml')

  print("Send location")
  return gr

if __name__ == "__main__":
  gr = register_message()
  app.run(host=hostname, port=port)
  print('The end')