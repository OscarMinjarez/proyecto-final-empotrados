from flask import Flask, request, jsonify
from flask_cors import CORS
from daos import *
from entidades import *
from conexion import mydb


app = Flask(__name__)
CORS(app)

dao_recipientes = RecipientesDAO(mydb)
dao_cantidades = CantidadesDAO(mydb)
PORT = 3000


@app.route('/recipientes', methods=['GET', 'POST'])
def gestionar_recipientes():
    if request.method == 'GET':
        recipientes = dao_recipientes.obtener_todos()
        return jsonify(recipientes)
    elif request.method == 'POST':
        datos_recipiente = request.json
        nuevo_recipiente = Recipiente(datos_recipiente['nombre_recipiente'], datos_recipiente['longitud'])
        dao_recipientes.crear(nuevo_recipiente)
        return jsonify({
            "mensaje": "Recipiente creado correctamente",
            "recipiente": {
                "recipiente_id": nuevo_recipiente.recipiente_id,
                "nombre_recipiente": nuevo_recipiente.nombre_recipiente,
                "longitud": nuevo_recipiente.longitud
            }
        }), 201


@app.route('/cantidades', methods=['GET', 'POST'])
def gestionar_cantidades():
    if request.method == 'GET':
        cantidades = dao_cantidades.obtener_todos()
        return jsonify(cantidades)
    elif request.method == 'POST':
        datos_cantidad = request.json
        nueva_cantidad = Cantidad(datos_cantidad['cantidad'], datos_cantidad['recipiente_id'])
        dao_cantidades.crear(nueva_cantidad)
        return jsonify({
            "mensaje": "Cantidad creada correctamente",
            "cantidad": {
                "cantidad_id": nueva_cantidad.cantidad_id,
                "cantidad": nueva_cantidad.cantidad,
                "fecha": nueva_cantidad.fecha,
                "recipiente_id": nueva_cantidad.recipiente_id
            }
        }), 201


def run():
    app.run(host = "0.0.0.0", port = PORT)