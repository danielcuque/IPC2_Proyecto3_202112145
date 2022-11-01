from typing import List
import xmltodict
from xml.dom.minidom import Element, parse, parseString
from flask import Flask, jsonify, request


from helpers.utils import allowed_file, read_info, create_elements

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
    with open('store.xml', 'r') as file:
        data = xmltodict.parse(file.read())
    return jsonify(data.get('store')), 200


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
        instances_created: int = 0

        data = request.files.getlist('')
        for file in data:
            if file and allowed_file(file.filename):
                quantities: int = read_info(file)
                resources_created += quantities[0]
                categories_created += quantities[1]
                clients_created += quantities[2]
                instances_created += quantities[3]

        return jsonify({
            'Clientes creados': clients_created,
            'Recursos creados': resources_created,
            'Categorias creadas': categories_created,
            'Instancias creadas': instances_created
        })

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


@app.route('/crearConsumos', methods=['POST'])
def consumos():
    if request.method == 'POST':
        files = request.files.getlist('')
        if len(files) == 0:
            return jsonify({'msg': 'No se encontraron archivos'}), 400

        petitions: int = 0
        for file in files:
            if file and allowed_file(file.filename):
                information_file: str = file.stream.read().decode('utf-8')
                config_info: Element = parseString(information_file)
                store: Element = parse('store.xml')
                petition_list: List[Element] = config_info.getElementsByTagName(
                    'listadoConsumos')[0].getElementsByTagName('consumo')
                petitions += create_elements(petition_list,
                                             store, 'listaConsumos')
                with open('store.xml', 'w') as file:
                    store.writexml(file)
    return jsonify({'consumos': petitions})


@app.route('/generarFactura', methods=['POST'])
def generarFactura():
    if not request.json or not 'nombre' in request.json:
        pass
    return jsonify({'nombre': request.json['nombre']}), 201


if __name__ == '__main__':
    app.run(debug=True)
