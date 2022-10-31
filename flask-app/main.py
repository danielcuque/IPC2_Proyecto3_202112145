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
        clients_created: int = 0
        resources_created: int = 0
        categories_created: int = 0

        data = request.files.getlist('')
        for file in data:
            if file and allowed_file(file.filename):
                quantities: int = read_info(file)
                clients_created += quantities[0]
                resources_created += quantities[1]
                categories_created += quantities[2]
        return jsonify({'clientes': clients_created, 'recursos': resources_created, 'categorias': categories_created}), 201
    return jsonify({'msg': 'No se pudo crear la configuración'}), 400


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
