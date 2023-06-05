__author__ = 'quimtorra'

from socket import gethostname
import socket
from flask import Flask, request, Response
from flask.json import jsonify
import json
import argparse
from rdflib import FOAF, RDF, Graph, Literal, Namespace
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
  if accion == ECSDI.Pedir_plan_viaje:        
    destino = gm.value(subject=content, predicate=ECSDI.Destino)
    data_ini = gm.value(subject=content, predicate=ECSDI.Data_Ini)
    data_fi = gm.value(subject=content, predicate=ECSDI.Data_Fi)
    presupuesto = gm.value(subject=content, predicate=ECSDI.Presupuesto)
    pref_Transportes = eval(gm.value(subject=content, predicate=ECSDI.Preferencias_Medio_Transporte))

    if len(pref_Transportes) != 0 : 
      res = pref_Transportes[random.randint(0, len(pref_Transportes)-1)]
      gr = build_message(Graph(),
                        ACL['inform'],
                        sender=AgenciaTransporte.uri,
                        content=Literal(res)).serialize(format='xml')
    else:  
      gr = build_message(Graph(),
                          ACL['inform'],
                          sender=AgenciaTransporte.uri,
                          content=Literal("NO OPTIONS AVAILABLE")).serialize(format='xml')
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