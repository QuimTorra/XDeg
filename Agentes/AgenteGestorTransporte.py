# -*- coding: utf-8 -*-

import argparse
from multiprocessing import Process, Queue
import socket

from rdflib import Namespace, Graph
from flask import Flask

from AgentUtil.FlaskServer import shutdown_server
from AgentUtil.Agent import Agent

__author__ = 'ori'

import argparse
import socket

from XDeg.AgentUtil.Logging import config_logger


parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, help="Puerto de comunicacion del agente.")
parser.add_argument("--host", default="localhost", help="Host agente.")
parser.add_argument("--open", default=False, help="Define si el servidor esta abierto al exterior o no.", action="store_true")
parser.add_argument("--dhost", default=socket.gethostname(), help="Host del agente de directorio.")
parser.add_argument("--dport", type=int, help="Puerto de comunicación del agente de directorio.", action="store_true")


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

AgentePersonal = Agent('AgenteSimple',
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
