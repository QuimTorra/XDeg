# -*- coding: utf-8 -*-

import argparse
from multiprocessing import Process, Queue
import socket

from rdflib import RDF, Namespace, Graph
from flask import Flask, request

from AgentUtil.FlaskServer import shutdown_server
from AgentUtil.Agent import Agent
from AgentUtil.ACLMessages import build_message
from AgentUtil import ACL
from AgentUtil.ACLMessages import get_message_properties

__author__ = 'ori'

import argparse
import socket

from AgentUtil.Logging import config_logger


# parser = argparse.ArgumentParser()
# parser.add_argument("--port", type=int, help="Puerto de comunicacion del agente.")
# parser.add_argument("--host", default="localhost", help="Host agente.")
# parser.add_argument("--open", default=False, help="Define si el servidor esta abierto al exterior o no.", action="store_true")
# parser.add_argument("--dhost", default=socket.gethostname(), help="Host del agente de directorio.")
# parser.add_argument("--dport", type=int, help="Puerto de comunicación del agente de directorio.", action="store_true")

# Definimos los parametros de la linea de comandos
parser = argparse.ArgumentParser()
parser.add_argument('--host', default='localhost', help="Host del agente")
parser.add_argument('--port', type=int, help="Puerto de comunicacion del agente")
parser.add_argument('--acomm', help='Direccion del agente con el que comunicarse')
parser.add_argument('--aport', type=int, help='Puerto del agente con el que comunicarse')
parser.add_argument('--messages', nargs='+', default=[], help="mensajes a enviar")


logger = config_logger(level=1)

args = parser.parse_args()

# Configuracion

if args.port is None:
    port = 9011
else:
    port = args.port

if args.open in None:
    hostname = "0.0.0.0"
else:
    hostname = socket.gethostname()

if args.dport is None:
    dport = 9000
else:
    dport = args.dport

# Configuration stuff
hostname = socket.gethostname()
port = 9010

agn = Namespace("http://www.agentes.org#")

# Contador de mensajes
mss_cnt = 0

# Datos del Agente

AgenteGestorTransporte = Agent('AgenteGestorTransporte',
                       agn.AgenteSimple,
                       'http://%s:%d/comm' % (hostname, port),
                       'http://%s:%d/Stop' % (hostname, port))

# Directory agent address
DirectoryAgent = Agent('DirectoryAgent',
                       agn.Directory,
                       'http://%s:9000/Register' % hostname,
                       'http://%s:9000/Stop' % hostname)

# Global triplestore graph
dsgraph = Graph()

cola1 = Queue()

# Flask stuff
app = Flask(__name__)


@app.route("/comm")
def comunicacion():
    """
    Entrypoint de comunicacion
    """
    global dsgraph
    global mss_cnt

    message = request.args["content"]
    gm = Graph()
    gm.parse(data=message)

    msgdic = get_message_properties(gm)

    # Comprobamos que sea un mensaje FIPA ACL
    if msgdic is None:
        # Si no es, respondemos que no hemos entendido el mensaje
        gr = build_message(Graph(), ACL['not-understood'], sender=AgenteGestorTransporte.uri, msgcnt=mss_cnt)
    else:
        # Obtenemos la performativa
        perf = msgdic['performative']
        if perf != ACL.request:
            # Si no es un request, respondemos que no hemos entendido el mensaje
            gr = build_message(Graph(), ACL['not-understood'], sender=AgenteGestorTransporte.uri, msgcnt=mss_cnt)
        else:
            # Extraemos el objeto del contenido que ha de ser una accion de la ontologia de acciones del agente
            # de registro
            # Averiguamos el tipo de la accion
            if 'content' in msgdic:
                content = msgdic['content']
                accion = gm.value(subject=content, predicate=RDF.type)
                # Aqui realizariamos lo que pide la accion
                # for s,p,o in gm:
                #     print("EOOO: %s | %s | %s"%(s,p,o))

                # if accion == AM2.Add_producto_externo: 
                #     logger.info("Petición de nuevo producto externo a añadir")
                #     resp = Graph()
                #     # resp = addProductoExterno(gm)

                #     gr = build_message(resp,
                #         ACL['inform-done'],
                #         sender=AgenteGestorTransporte.uri,
                #         msgcnt=mss_cnt,
                #         receiver=msgdic['sender'], )
                # else:
                #     gr = build_message(Graph(), ACL['not-understood'], sender=AgenteGestorTransporte.uri, msgcnt=mss_cnt)
            else:
                gr = build_message(Graph(), ACL['not-understood'], sender=AgenteGestorTransporte.uri, msgcnt=mss_cnt)

    mss_cnt += 1
    logger.info('Respondemos a la solicitud nuevo producto externo')
    return gr.serialize(format='xml')

    pass


@app.route("/Stop")
def stop():
    """
    Entrypoint que para el agente

    :return:
    """
    tidyup()
    shutdown_server()
    return "Parando Servidor"


def tidyup():
    """
    Acciones previas a parar el agente

    """
    pass


def agentbehavior1(cola):
    """
    Un comportamiento del agente

    :return:
    """
    pass


if __name__ == '__main__':
    # Ponemos en marcha los behaviors
    ab1 = Process(target=agentbehavior1, args=(cola1,))
    ab1.start()

    # Ponemos en marcha el servidor
    app.run(host=hostname, port=port)

    # Esperamos a que acaben los behaviors
    ab1.join()
    print('The End')
