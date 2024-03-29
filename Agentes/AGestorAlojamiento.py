# -*- coding: utf-8 -*-
"""
filename: AgenteGestorAlojamiento

Antes de ejecutar hay que añadir la raiz del proyecto a la variable PYTHONPATH

Agente que se registra como agente de Gestor de Transporte y espera peticiones

@author: xDeg
"""

from multiprocessing import Process, Queue
import logging
import argparse

from flask import Flask, request
from rdflib import XSD, Graph, Namespace, Literal
from rdflib.namespace import FOAF, RDF
import requests

from AgentUtil.ACL import ACL
from AgentUtil.FlaskServer import shutdown_server
from AgentUtil.ACLMessages import build_message, send_message, get_message_properties
from AgentUtil.Agent import Agent
from AgentUtil.Logging import config_logger
from AgentUtil.DSO import DSO
from AgentUtil.Util import gethostname
import socket

from AgentUtil.OntoNamespaces import ECSDI


__author__ = 'xDeg'

# Definimos los parametros de la linea de comandos
parser = argparse.ArgumentParser()
parser.add_argument('--open', help="Define si el servidor esta abierto al exterior o no", action='store_true',
                    default=False)
parser.add_argument('--verbose', help="Genera un log de la comunicacion del servidor web", action='store_true',
                        default=False)
parser.add_argument('--port', type=int, help="Puerto de comunicacion del agente")
parser.add_argument('--dhost', help="Host del agente de directorio")
parser.add_argument('--dport', type=int, help="Puerto de comunicacion del agente de directorio")
parser.add_argument('--ahost', help="Host del agente externo con el que comunicarse")
parser.add_argument('--aport', type=int, help="Puerto de comunicacion del agente externo con el que comunicarse")


# Logging
logger = config_logger(level=1)

# parsing de los parametros de la linea de comandos
args = parser.parse_args()

# Configuration stuff
if args.port is None:
    port = 9012
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

if args.aport is None:
    aport = 9051
else:
    aport = args.aport

if args.ahost is None:
    ahostname = socket.gethostname()
else:
    ahostname = args.ahost

# Flask stuff
app = Flask(__name__)
if not args.verbose:
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

# Configuration constants and variables
agn = Namespace("http://www.agentes.org#")

# Contador de mensajes
mss_cnt = 0

# Datos del Agente
GestorAlojamiento = Agent('GestorAlojamiento',
                  agn.GestorAlojamiento,
                  'http://%s:%d/comm' % (hostaddr, port),
                  'http://%s:%d/Stop' % (hostaddr, port))

# Directory agent address
DirectoryAgent = Agent('DirectoryAgent',
                       agn.Directory,
                       'http://%s:%d/Register' % (dhostname, dport),
                       'http://%s:%d/Stop' % (dhostname, dport))

# Global dsgraph triplestore
dsgraph = Graph()

# Cola de comunicacion entre procesos
cola1 = Queue()


def register_message():
    """
    Envia un mensaje de registro al servicio de registro
    usando una performativa Request y una accion Register del
    servicio de directorio

    :param gmess:
    :return:
    """

    logger.info('Nos registramos')

    global mss_cnt

    gmess = Graph()

    # Construimos el mensaje de registro
    gmess.bind('foaf', FOAF)
    gmess.bind('dso', DSO)
    reg_obj = agn[GestorAlojamiento.name + '-Register']
    gmess.add((reg_obj, RDF.type, DSO.Register))
    gmess.add((reg_obj, DSO.Uri, GestorAlojamiento.uri))
    gmess.add((reg_obj, FOAF.name, Literal(GestorAlojamiento.name)))
    gmess.add((reg_obj, DSO.Address, Literal(GestorAlojamiento.address)))
    gmess.add((reg_obj, DSO.AgentType, DSO.GestorAlojamiento))

    # Lo metemos en un envoltorio FIPA-ACL y lo enviamos
    gr = send_message(
        build_message(gmess, perf=ACL.request,
                      sender=GestorAlojamiento.uri,
                      receiver=DirectoryAgent.uri,
                      content=reg_obj,
                      msgcnt=mss_cnt),
        DirectoryAgent.address)
    mss_cnt += 1

    return gr


@app.route("/iface", methods=['GET', 'POST'])
def browser_iface():
    """
    Permite la comunicacion con el agente via un navegador
    via un formulario
    """
    return 'This is a Transport Manager. Nothing to see here'


@app.route("/stop")
def stop():
    """
    Entrypoint que para el agente

    :return:
    """
    tidyup()
    shutdown_server()
    return "Parando Servidor"


@app.route("/comm")
def comunicacion():
    """
    Entrypoint de comunicacion del agente
    Simplemente retorna un objeto fijo que representa una
    respuesta a una busqueda de hotel

    Asumimos que se reciben siempre acciones que se refieren a lo que puede hacer
    el agente (buscar con ciertas restricciones, reservar)
    Las acciones se mandan siempre con un Request
    Prodriamos resolver las busquedas usando una performativa de Query-ref
    """
    global dsgraph
    global mss_cnt

    logger.info('Peticion de informacion recibida')

    # Extraemos el mensaje y creamos un grafo con el
    message = request.args['content']

    gm = Graph()
    gm.parse(data=message, format='xml')

    msgdic = get_message_properties(gm)

    # Comprobamos que sea un mensaje FIPA ACL
    if msgdic is None:
        # Si no es, respondemos que no hemos entendido el mensaje
        gr = build_message(Graph(), ACL['not-understood'], sender=GestorAlojamiento.uri, msgcnt=mss_cnt)
    else:
        # Obtenemos la performativa
        perf = msgdic['performative']

        if perf != ACL.request:
            # Si no es un request, respondemos que no hemos entendido el mensaje
            gr = build_message(Graph(), ACL['not-understood'], sender=GestorAlojamiento.uri, msgcnt=mss_cnt)
        else:
            # Extraemos el objeto del contenido que ha de ser una accion de la ontologia de acciones del agente
            # de registro

            # Averiguamos el tipo de la accion
            if 'content' in msgdic:
                content = msgdic['content']
                accion = gm.value(subject=content, predicate=RDF.type)

            accion = gm.value(subject=content, predicate=RDF.type)
            if accion == ECSDI.Pedir_plan_viaje:        
                destino = gm.value(subject=content, predicate=ECSDI.Destino)
                data_ini = gm.value(subject=content, predicate=ECSDI.Data_Ini)
                data_fi = gm.value(subject=content, predicate=ECSDI.Data_Fi)
                min_estrellas = gm.value(subject=content, predicate=ECSDI.Estrellas)
                pref_alojamientos = gm.value(subject=content, predicate=ECSDI.Preferencias_Alojamiento)

                address = 'http://%s:%d/alojamiento' % (ahostname, aport)
                gg = Graph()
                tp_content = ECSDI['Pedir_plan_viaje']
                gg.add((tp_content, RDF.type, ECSDI.Pedir_alojamiento))
                gg.add((tp_content, ECSDI.Destino, Literal(destino)))
                gg.add((tp_content, ECSDI.Data_Ini, Literal(data_ini)))
                gg.add((tp_content, ECSDI.Data_Fi, Literal(data_fi)))
                gg.add((tp_content, ECSDI.Preferencias_Alojamiento, Literal(pref_alojamientos)))
                deg = build_message(gg,
                                  ACL.request,
                                  sender=GestorAlojamiento.uri,
                                  msgcnt=mss_cnt,
                                  content=tp_content)
                r = send_message(deg, address)
                rm = get_message_properties(r)
                content = rm['content']

                if content.toPython() == "OPTIONS AVAILABLE":
                    lowest_price = 10000000
                    
                    #search for best price
                    for alojamiento in r.subjects(RDF.type, ECSDI.Alojamiento):
                        
                        if lowest_price > r.value(subject=alojamiento, predicate=ECSDI.Precio).toPython() \
                            and r.value(subject=alojamiento, predicate=ECSDI.Nombre).toPython() in pref_alojamientos \
                                and r.value(subject=alojamiento, predicate=ECSDI.Estrellas).toPython() > min_estrellas.toPython():
                            lowest_subject = alojamiento
                            lowest_name = r.value(subject=alojamiento, predicate=ECSDI.Nombre)
                            lowest_price = r.value(subject=alojamiento, predicate=ECSDI.Precio).toPython()
                            lowest_star = r.value(subject=alojamiento, predicate=ECSDI.Estrellas).toPython()
                    
                    grespuesta = Graph()
                    grespuesta.add((lowest_subject, RDF.type, ECSDI.Alojamiento))
                    grespuesta.add((lowest_subject, ECSDI.Nombre, Literal(lowest_name, datatype=XSD.string)))
                    grespuesta.add((lowest_subject, ECSDI.Precio, Literal(lowest_price, datatype=XSD.integer)))
                    grespuesta.add((lowest_subject, ECSDI.Estrellas, Literal(lowest_star, datatype=XSD.integer)))

                    print("#### RESULTADO QUERY ####")
                    for alojamiento in grespuesta.subjects(RDF.type, ECSDI.Alojamiento):
                        print(destino,
                            grespuesta.value(subject=alojamiento, predicate=ECSDI.Nombre),
                            grespuesta.value(subject=alojamiento, predicate=ECSDI.Precio),
                            grespuesta.value(subject=alojamiento, predicate=ECSDI.Estrellas))
                    
                    #SEND BEST OPTION CALCULATED
                    gr = Graph()
                    gr = build_message(grespuesta,
                            ACL['inform'],
                            sender=GestorAlojamiento.uri,
                            content=content).serialize(format='xml')
                else:
                    gr = build_message(Graph(),
                        ACL['inform'],
                        sender=GestorAlojamiento.uri,
                        content=Literal("NO OPTIONS AVAILABLE")).serialize(format='xml')

            else:
                gr = build_message(Graph(),
                        ACL['inform'],
                        sender=GestorAlojamiento.uri,
                        content=Literal("NO ENTIENDO")).serialize(format='xml')

    mss_cnt += 1

    logger.info('Respondemos a la peticion')

    return gr




def tidyup():
    """
    Acciones previas a parar el agente

    """
    global cola1
    cola1.put(0)


def agentbehavior1(cola):
    """
    Un comportamiento del agente

    :return:
    """
    # Registramos el agente
    gr = register_message()

    # Escuchando la cola hasta que llegue un 0
    fin = False
    while not fin:
        while cola.empty():
            pass
        v = cola.get()
        if v == 0:
            fin = True
        else:
            print(v)



if __name__ == '__main__':
    # Ponemos en marcha los behaviors
    ab1 = Process(target=agentbehavior1, args=(cola1,))
    ab1.start()

    # Ponemos en marcha el servidor
    app.run(host=hostname, port=port)

    # Esperamos a que acaben los behaviors
    ab1.join()
    logger.info('The End')
