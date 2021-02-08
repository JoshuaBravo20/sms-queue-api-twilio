"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from twilio.rest import Client
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate, MigrateCommand
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import Queue
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

newQ = Queue() # INSTANCIA NUEVA Y UNICA DE LA CLASE QUEUE

@app.route('/new', methods=['POST'])
def handleNew(): # RECIBE DATOS Y LOS TRANSFIERE A ENQUEUE()

    name = request.json.get('name') # CAPTURAR VALOR DE NOMBRE

    if not name: # VALIDAR NOMBRE
        return jsonify({"msg": "name is required"}), 400

    item = {
        "name": name
    } # DEFINIR EL DICT

    newQ.enqueue(item) # APLICAR LA FUNCIÓN DE INGRESAR A LA FILA

    return jsonify({"sent": "message has been sent!"}), 201



@app.route('/all', methods=['GET'])
def getAll(): # RETORNA LA FILA ENTERA

    q = newQ.get_queue() # APLICAR FUNCION DE RETORNAR FILA ENTERA A LA INSTANCIA
    return jsonify(q), 200 



@app.route('/next', methods=['GET'])
def handleNext():
    nextq = newQ.dequeue() # APLICAR DEQUEUE A A LA INSTANCIA
    return jsonify({"msg": "processed! next in line is..."}, nextq), 200






# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
