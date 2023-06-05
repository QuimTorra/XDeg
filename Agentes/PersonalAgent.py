# -*- coding: utf-8 -*-
"""
filename: SimplePersonalAgent

Antes de ejecutar hay que añadir la raiz del proyecto a la variable PYTHONPATH

Ejemplo de agente que busca en el directorio y llama al agente obtenido


Created on 09/02/2014

@author: javier
"""

from multiprocessing import Process
import logging
import argparse

from flask import Flask, render_template, request
from rdflib import Graph, Literal, Namespace, XSD, URIRef
from rdflib.namespace import FOAF, RDF

from AgentUtil.ACL import ACL
from AgentUtil.DSO import DSO
from AgentUtil.FlaskServer import shutdown_server
from AgentUtil.ACLMessages import build_message, send_message
from AgentUtil.Agent import Agent
from AgentUtil.Logging import config_logger
from AgentUtil.Util import gethostname
from AgentUtil.OntoNamespaces import ECSDI
import socket

from AgentUtil.ACLMessages import get_message_properties
from AGestorTransporte import GestorTransporte

__author__ = 'javier'

# Definimos los parametros de la linea de comandos
parser = argparse.ArgumentParser()
parser.add_argument('--open', help="Define si el servidor est abierto al exterior o no", action='store_true',
                    default=False)
parser.add_argument('--verbose', help="Genera un log de la comunicacion del servidor web", action='store_true',
                        default=False)
parser.add_argument('--port', type=int, help="Puerto de comunicacion del agente")
parser.add_argument('--dhost', help="Host del agente de directorio")
parser.add_argument('--dport', type=int, help="Puerto de comunicacion del agente de directorio")

# Logging
logger = config_logger(level=1)

# parsing de los parametros de la linea de comandos
args = parser.parse_args()

# Configuration stuff
if args.port is None:
    port = 9001
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
AgentePersonal = Agent('AgentePersonal',
                       agn.AgentePersonal,
                       'http://%s:%d/comm' % (hostaddr, port),
                       'http://%s:%d/Stop' % (hostaddr, port))

# Directory agent address
DirectoryAgent = Agent('DirectoryAgent',
                       agn.Directory,
                       'http://%s:%d/Register' % (dhostname, dport),
                       'http://%s:%d/Stop' % (dhostname, dport))

# Global dsgraph triplestore
dsgraph = Graph()

def directory_search_message(type):
    """
    Busca en el servicio de registro mandando un
    mensaje de request con una accion Seach del servicio de directorio

    Podria ser mas adecuado mandar un query-ref y una descripcion de registo
    con variables

    :param type:
    :return:
    """
    global mss_cnt
    logger.info('Buscamos en el servicio de registro')

    gmess = Graph()

    gmess.bind('foaf', FOAF)
    gmess.bind('dso', DSO)
    reg_obj = agn[AgentePersonal.name + '-search']
    gmess.add((reg_obj, RDF.type, DSO.Search))
    gmess.add((reg_obj, DSO.AgentType, type))

    msg = build_message(gmess, perf=ACL.request,
                        sender=AgentePersonal.uri,
                        receiver=DirectoryAgent.uri,
                        content=reg_obj,
                        msgcnt=mss_cnt)
    gr = send_message(msg, DirectoryAgent.address)
    mss_cnt += 1
    logger.info('Recibimos informacion del agente')

    return gr


def infoagent_search_message(addr, ragn_uri, content):
    """
    Envia una accion a un agente de informacion
    """
    global mss_cnt
    logger.info('Hacemos una peticion al servicio de informacion')

    gmess = Graph()

    # Supuesta ontologia de acciones de agentes de informacion
    IAA = Namespace('IAActions')

    gmess.bind('foaf', FOAF)
    gmess.bind('iaa', IAA)
    reg_obj = agn[AgentePersonal.name + '-info-search']
    gmess.add((reg_obj, RDF.type, IAA.Search))

    msg = build_message(gmess, perf=ACL.request,
                        sender=AgentePersonal.uri,
                        receiver=ragn_uri,
                        msgcnt=mss_cnt,
                        content=content)
    gr = send_message(msg, addr)
    mss_cnt += 1
    logger.info('Recibimos respuesta a la peticion al servicio de informacion')

    return gr

def get_count():
    global mss_cnt
    if not mss_cnt:
        mss_cnt = 0
    mss_cnt += 1
    return mss_cnt

@app.route("/iface", methods=['GET', 'POST'])
def browser_iface():
    """
    Permite la comunicacion con el agente via un navegador
    via un formulario
    """
    if request.method == 'GET':
        return render_template('iface.html')
    else:
        user = request.form['username']
        mess = request.form['message']
        return render_template('riface.html', user=user, mess=mess)


@app.route("/plan", methods=['GET', 'POST'])
def hacer_plan():
    if request.method == 'GET':
        return render_template('plan.html')
    else:
        gr = directory_search_message(DSO.GestorTransporte)
        msg = gr.value(predicate=RDF.type, object=ACL.FipaAclMessage)
        content = gr.value(subject=msg, predicate=ACL.content)
        ragn_addr = gr.value(subject=content, predicate=DSO.Address)
        
        #GET INFO FORM
        destination = request.form['tp_destination']
        date_Ini = request.form['dateIni']
        date_Fi = request.form['dateEnd'] 
        presupost = request.form['presupost']
        pref_trans =  []
        if 'tp_bus' in request.form: pref_trans.append('bus')
        if 'tp_plane' in request.form: pref_trans.append('plane')
        if 'tp_train' in request.form: pref_trans.append('train')
        if 'tp_ferry' in request.form: pref_trans.append('ferry')

        #Peticion Viaje
        gr = Graph()
        contentResult = ECSDI['Pedir_plan_viaje_'+ str(get_count())]
        gr.add((contentResult, RDF.type, ECSDI.Pedir_plan_viaje))
        gr.add((contentResult, ECSDI.Destino, Literal(destination, datatype=XSD.string)))
        gr.add((contentResult, ECSDI.Data_Ini, Literal(date_Ini, datatype=XSD.date)))
        gr.add((contentResult, ECSDI.Data_Fi, Literal(date_Fi, datatype=XSD.date)))
        gr.add((contentResult, ECSDI.Presupuesto, Literal(presupost, datatype=XSD.integer)))
        gr.add((contentResult, ECSDI.Preferencias_Medio_Transporte, Literal(str(pref_trans), datatype=XSD.string)))

        deg = build_message(gr,
                               ACL['request'],
                               sender=AgentePersonal.uri,
                               receiver=GestorTransporte.uri,
                               content=contentResult,
                               msgcnt=get_count(),)
        rr = send_message(deg, ragn_addr)
        msgdic = get_message_properties(rr)
        transport = msgdic['content']

        return render_template('rplan.html', transport=transport)


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
    """
    return "Hola"


def tidyup():
    """
    Acciones previas a parar el agente

    """
    pass


def agentbehavior1():
    """
    Un comportamiento del agente

    :return:
    """

    # # Buscamos en el directorio
    # # un agente de hoteles
    # gr = directory_search_message(DSO.GestorTransporte)

    # # Obtenemos la direccion del agente de la respuesta
    # # No hacemos ninguna comprobacion sobre si es un mensaje valido
    # msg = gr.value(predicate=RDF.type, object=ACL.FipaAclMessage)
    # content = gr.value(subject=msg, predicate=ACL.content)
    # ragn_addr = gr.value(subject=content, predicate=DSO.Address)
    # ragn_uri = gr.value(subject=content, predicate=DSO.Uri)

    # # Ahora mandamos un objeto de tipo request mandando una accion de tipo Search
    # # que esta en una supuesta ontologia de acciones de agentes
    # gg = infoagent_search_message(ragn_addr, ragn_uri)
    # msgdic = get_message_properties(gg)
    # print(msgdic["content"])

if __name__ == '__main__':
    # Ponemos en marcha los behaviors
    ab1 = Process(target=agentbehavior1)
    ab1.start()

    # Ponemos en marcha el servidor
    app.run(host=hostname, port=port)

    # Esperamos a que acaben los behaviors
    ab1.join()
    logger.info('The End')
