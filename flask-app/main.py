from flask import Flask, jsonify, request


from helpers.utils import allowed_file, read_info

app = Flask(__name__)


@app.route('/')
def index():
    initial_message = {
        "msg": 'Servidor funcionando correctamente',
        "status": 200
    }

    return jsonify(initial_message)


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


@app.route('/crearConfiguracion', methods=['POST'])
def crearConfiguracion():
    if request.method == 'POST':
        data = request.files.getlist('')
        for file in data:
            if file and allowed_file(file.filename):
                read_info(file)
    return 'ok', 200


@app.route('/crearCliente', methods=['POST'])
def crearCliente():
    if not request.json or not 'nombre' in request.json:
        pass
    return jsonify({'nombre': request.json['nombre']}), 201


@app.route('/crearInstancia', methods=['POST'])
def crearInstancia():
    if not request.json or not 'nombre' in request.json:
        pass
    return jsonify({'nombre': request.json['nombre']}), 201


@app.route('/generarFactura', methods=['POST'])
def generarFactura():
    if not request.json or not 'nombre' in request.json:
        pass
    return jsonify({'nombre': request.json['nombre']}), 201


if __name__ == '__main__':
    app.run(debug=True)
