from crypt import methods
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/consultarDatos', methods=['GET'])
def consultarDatos():
    return jsonify({'datos': 'datos'})

@app.route('/crearRecurso', methods=['POST'])
def crearRecurso():
    if not request.json or not 'nombre' in request.json:
        pass
    return jsonify({'nombre': request.json['nombre']}), 201

@app.route('/crearCategoria', methods=['POST'])
def crearCategoria():
    if not request.json or not 'nombre' in request.json:
        pass
    return jsonify({'nombre': request.json['nombre']}), 201


if __name__ == '__main__':
    app.run(debug=True)
