# -*- coding: utf-8 -*-
"""
filename: AgenteOrganizador 

Antes de ejecutar hay que añadir la raiz del proyecto a la variable PYTHONPATH

Agente que se comunica con otros agentes para organizar un viaje para un determinado usuario.

@author: xDeg
"""

from multiprocessing import Process, Manager, Value, Queue
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
from ctypes import c_char_p

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
    port = 9010
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
    aport = 9050
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
AgenteOrganizador = Agent('AgenteOrganizador',
                  agn.AgenteOrganizador,
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

def find_agent_info(type):
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
    reg_obj = agn[AgenteOrganizador.name + '-search']
    gmess.add((reg_obj, RDF.type, DSO.Search))
    gmess.add((reg_obj, DSO.AgentType, type))

    msg = build_message(gmess, perf=ACL.request,
                        sender=AgenteOrganizador.uri,
                        receiver=DirectoryAgent.uri,
                        content=reg_obj,
                        msgcnt=mss_cnt)
    gr = send_message(msg, DirectoryAgent.address)
    mss_cnt += 1
    logger.info('Recibimos informacion del agente')

    return gr

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
    reg_obj = agn[AgenteOrganizador.name + '-Register']
    gmess.add((reg_obj, RDF.type, DSO.Register))
    gmess.add((reg_obj, DSO.Uri, AgenteOrganizador.uri))
    gmess.add((reg_obj, FOAF.name, Literal(AgenteOrganizador.name)))
    gmess.add((reg_obj, DSO.Address, Literal(AgenteOrganizador.address)))
    gmess.add((reg_obj, DSO.AgentType, DSO.AgenteOrganizador))

    # Lo metemos en un envoltorio FIPA-ACL y lo enviamos
    gr = send_message(
        build_message(gmess, perf=ACL.request,
                      sender=AgenteOrganizador.uri,
                      receiver=DirectoryAgent.uri,
                      content=reg_obj,
                      msgcnt=mss_cnt),
        DirectoryAgent.address)
    mss_cnt += 1

    return gr

#FUNCTION FOR SUBPROCESS TRANSPORTE
def run_pedir_transporte(transport_name, transport_price, destino, data_ini, data_fi, pref_Transportes):
    transport_name.value, transport_price.value = pedir_transporte(destino, data_ini, data_fi, pref_Transportes)
    #print(transport_name.value, transport_price.value)

#FUNCTION FOR SUBPROCESS ALOJAMIENTO
def run_pedir_alojamiento(alojam_name, alojam_price, alojam_estrellas, destino, data_ini, data_fi, pref_Alojamientos, min_estrellas):
    alojam_name.value, alojam_price.value, alojam_estrellas.value = pedir_alojamiento(destino, data_ini, data_fi, pref_Alojamientos, min_estrellas)
    #print(alojam_name.value, alojam_price.value, alojam_estrellas.value)

#FUNCTION FOR SUBPROCESS ACTIVIDADES
def run_pedir_actividades(actividades_result, destino, data_ini, data_fi, presupuesto):
    actividades_result.value = pedir_actividades(destino, data_ini, data_fi, presupuesto)
    #print(actividades_result.value)


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
    content = msgdic['content']

    accion = gm.value(subject=content, predicate=RDF.type)
    if accion == ECSDI.Pedir_plan_viaje:        
        destino = gm.value(subject=content, predicate=ECSDI.Destino)
        gente = gm.value(subject=content, predicate=ECSDI.Gente)
        data_ini = gm.value(subject=content, predicate=ECSDI.Data_Ini)
        data_fi = gm.value(subject=content, predicate=ECSDI.Data_Fi)
        presupuesto = gm.value(subject=content, predicate=ECSDI.Presupuesto)
        pref_Transportes = eval(gm.value(subject=content, predicate=ECSDI.Preferencias_Medio_Transporte))
        pref_Alojamientos = eval(gm.value(subject=content, predicate=ECSDI.Preferencias_Alojamiento))
        min_estrellas = eval(gm.value(subject=content, predicate=ECSDI.Estrellas))

        if (data_fi < data_ini):
            print("invalid date")
            error_graph = Graph()
            res_content = ECSDI['Pedir_plan_viaje']
            mensaje_error = "Las fechas seleccionadas son inválidas."
            error_graph.add((res_content, RDF.type, ECSDI.Pedir_plan_viaje))
            error_graph.add((res_content, ECSDI.mensaje_error, Literal(mensaje_error)))
            gr = build_message(error_graph,
                            ACL['inform'],
                            sender=AgenteOrganizador.uri,
                            msgcnt=mss_cnt,
                            receiver=msgdic['sender'],
                            content=res_content)

            mss_cnt += 1
            return gr.serialize(format='xml')

        # RETURN VARIABLES FOR SUBROCESSING
        manager = Manager()
        transport_name = manager.Value(c_char_p, "NONE")
        transport_price = manager.Value('i', 0) 
        alojam_name = manager.Value(c_char_p, 'NONE')
        alojam_price = manager.Value('i', 0)
        alojam_estrellas = manager.Value('i', 0)
        actividades_result = manager.Value(c_char_p,'NONE')

        # Buscamos transporte, Alojamiento i Actividades
        transport_process = Process(target=run_pedir_transporte, args=(transport_name, transport_price, destino, data_ini, data_fi, pref_Transportes))
        alojamiento_process = Process(target=run_pedir_alojamiento, args=(alojam_name, alojam_price, alojam_estrellas, destino, data_ini, data_fi, pref_Alojamientos, min_estrellas))
        actividades_process = Process(target=run_pedir_actividades, args=(actividades_result, destino, data_ini, data_fi, presupuesto))

        #Start suprocess
        transport_process.start()
        alojamiento_process.start()
        actividades_process.start()

        # Wait for process to finish
        transport_process.join()
        alojamiento_process.join()
        actividades_process.join()

        #results
        print(transport_name.value, transport_price.value)
        print(alojam_name.value, alojam_price.value, alojam_estrellas.value)
        print(actividades_result.value)

        # Construimos la respuesta
        res_g = Graph()
        res_content = ECSDI['Pedir_plan_viaje']
        res_g.add((res_content, RDF.type, ECSDI.Pedir_plan_viaje))
        res_g.add((res_content, ECSDI.transport, Literal(transport_name.value)))
        res_g.add((res_content, ECSDI.transport_precio, Literal(transport_price.value)))
        res_g.add((res_content, ECSDI.alojamiento, Literal(alojam_name.value)))
        res_g.add((res_content, ECSDI.aloj_precio, Literal(alojam_price.value)))
        res_g.add((res_content, ECSDI.aloj_estrellas, Literal(alojam_estrellas.value)))
        res_g.add((res_content, ECSDI.actividades, Literal(actividades_result.value)))
        gr = build_message(res_g,
                            ACL['inform'],
                            sender=AgenteOrganizador.uri,
                            msgcnt=mss_cnt,
                            receiver=msgdic['sender'],
                            content=res_content)

    mss_cnt += 1


    logger.info('Respondemos a la peticion')

    return gr.serialize(format='xml')


def pedir_transporte(destino, data_ini, data_fi, pref_Transportes):
     # Buscamos Transporte
    gr = find_agent_info(DSO.GestorTransporte)
    msg = gr.value(predicate=RDF.type, object=ACL.FipaAclMessage)
    content = gr.value(subject=msg, predicate=ACL.content)
    trans_addr = gr.value(subject=content, predicate=DSO.Address)

    trans_g = Graph()
    tp_content = ECSDI['Pedir_plan_viaje']
    trans_g.add((tp_content, RDF.type, ECSDI.Pedir_plan_viaje))
    trans_g.add((tp_content, ECSDI.Destino, Literal(destino)))
    trans_g.add((tp_content, ECSDI.Data_Ini, Literal(data_ini)))
    trans_g.add((tp_content, ECSDI.Data_Fi, Literal(data_fi)))
    trans_g.add((tp_content, ECSDI.Preferencias_Medio_Transporte, Literal(pref_Transportes)))

    deg = build_message(trans_g,
                        ACL.request,
                        sender=AgenteOrganizador.uri,
                        msgcnt=mss_cnt,
                        content=tp_content)
    tp_res = send_message(deg, trans_addr)
    rm = get_message_properties(tp_res)
    transport = rm['content']
    if transport.toPython() == "OPTIONS AVAILABLE":
        for medio_t in tp_res.subjects(RDF.type, ECSDI.Medio_De_Transporte):
            #There should only be one inside the list
            transport_name = tp_res.value(subject=medio_t, predicate=ECSDI.Nombre).toPython()
            transport_price = tp_res.value(subject=medio_t, predicate=ECSDI.Precio).toPython()
            return transport_name, transport_price
    return None, None

def pedir_alojamiento(destino, data_ini, data_fi, pref_Alojamientos, min_estrellas):
     # Buscamos Transporte
    gr = find_agent_info(DSO.GestorAlojamiento)
    msg = gr.value(predicate=RDF.type, object=ACL.FipaAclMessage)
    content = gr.value(subject=msg, predicate=ACL.content)
    aloj_addr = gr.value(subject=content, predicate=DSO.Address)

    aloj = Graph()
    aj_content = ECSDI['Pedir_plan_viaje']
    aloj.add((aj_content, RDF.type, ECSDI.Pedir_plan_viaje))
    aloj.add((aj_content, ECSDI.Destino, Literal(destino)))
    aloj.add((aj_content, ECSDI.Data_Ini, Literal(data_ini)))
    aloj.add((aj_content, ECSDI.Data_Fi, Literal(data_fi)))
    aloj.add((aj_content, ECSDI.Preferencias_Alojamiento, Literal(pref_Alojamientos)))
    aloj.add((aj_content, ECSDI.Estrellas, Literal(min_estrellas)))

    deg = build_message(aloj,
                        ACL.request,
                        sender=AgenteOrganizador.uri,
                        msgcnt=mss_cnt,
                        content=aj_content)
    aj_res = send_message(deg, aloj_addr)
    aj_m = get_message_properties(aj_res)
    aj_cont = aj_m['content']
    if aj_cont.toPython() == "OPTIONS AVAILABLE":
        for medio_t in aj_res.subjects(RDF.type, ECSDI.Alojamiento):
            #There should only be one inside the list
            aloj_name = aj_res.value(subject=medio_t, predicate=ECSDI.Nombre).toPython()
            aloj_price = aj_res.value(subject=medio_t, predicate=ECSDI.Precio).toPython()
            aloj_stars = aj_res.value(subject=medio_t, predicate=ECSDI.Estrellas).toPython()
            return aloj_name, aloj_price, aloj_stars
    return None, None, None

def pedir_actividades(destino, data_ini, data_fi, presupuesto) :

    gr_a = find_agent_info(DSO.GestorActividades)
    msg_a = gr_a.value(predicate=RDF.type, object=ACL.FipaAclMessage)
    content_a = gr_a.value(subject=msg_a, predicate=ACL.content)
    activ_addr = gr_a.value(subject=content_a, predicate=DSO.Address)
    
    activ_g = Graph()
    ac_content = ECSDI['Pedir_plan_viaje']
    activ_g.add((ac_content, RDF.type, ECSDI.Pedir_plan_viaje))
    activ_g.add((ac_content, ECSDI.Destino, Literal(destino)))
    activ_g.add((ac_content, ECSDI.Data_Ini, Literal(data_ini)))
    activ_g.add((ac_content, ECSDI.Data_Fi, Literal(data_fi)))
    activ_g.add((ac_content, ECSDI.Presupuesto, Literal(presupuesto, datatype=XSD.integer)))

    deg_a = build_message(activ_g,
                        ACL.request,
                        sender=AgenteOrganizador.uri,
                        msgcnt=mss_cnt,
                        content=ac_content)
    ac_res = send_message(deg_a, activ_addr)
    ac_m = get_message_properties(ac_res)
    ac_cont = ac_m['content']
    return ac_res.value(subject=ac_cont, predicate=ECSDI.actividades)


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
