import argparse
import random
import socket

from flask import Flask, request

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, help="Puerto del agente.")
parser.add_argument("--host", default="localhost", help="Host agente.")
parser.add_argument("--acomm", help="Direccion del agent con el que comunicarse.")
parser.add_argument("--aport", type=int, help="Puerto del agente con el que comunicarse.")
parser.add_argument("--messages", nargs="+", default=[], help="Mensajes a enviar.")



app = Flask(__name__)

tiposTransportes = ["avión", "barco", "tren", "bus"]

@app.route("/")
def index():
    text = "Agencia de transportes. Para obtener el medio de transporte ideal para tu viaje ve a https://localhost:5000/transportes."

@app.route("/transportes")
def transportes():
    destinacion = request.args["destinacion"]
    fechaSalida = request.args["fechaSalida"]
    fechaVuelta = request.args["fechaVuelta"]
    origen = request.args["origen"]
    precioMaximo = request.args["precioMaximo"]
    respuesta = tiposTransportes[random.randint(0,3)]

    return respuesta

if __name__ == "__main__":
    args = parser.parse_args()
    app.run(host=args.host, port=9100)
    print("The End")



