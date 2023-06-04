__author__ = 'quimtorra'

from socket import gethostname
import socket
from flask import Flask, request, Response
from flask.json import jsonify
import json
import argparse
import requests
from requests import ConnectionError
from multiprocessing import Process
import string
import random

# Definimos los parametros de la linea de comandos
parser = argparse.ArgumentParser()
parser.add_argument('--host', default='localhost', help="Host del agente")
parser.add_argument('--port', type=int,  help="Puerto de comunicacion del agente")
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

app = Flask(__name__)

available = ["bus", "plane", "train", "ferry"]

@app.route("/")
def isAlive():
  text = 'Hi i\'m AExtTransporte o/, if you wanna travel go to <a href= /transport?coses=deg>here</a>'
  return text

@app.route("/transport")
def getTransport():
  # host:port/transport
  print(request.args["coses"])
  return available[random.randint(0, len(available)-1)]

if __name__ == "__main__":
  app.run(host=hostname, port=port)
  print('The end')