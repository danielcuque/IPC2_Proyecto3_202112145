import os
import xmltodict
from typing import List
from xml.dom.minidom import Element, parse, parseString
from flask import Flask, jsonify, request


from helpers.utils import allowed_file, read_info, create_elements, create_clients

app = Flask(__name__)

if os.path.exists('store.xml'):
    store: Element = parse('store.xml')


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
    if request.method == 'POST':
        new_resource: str = request.data.decode('utf-8')
        new_resource: Element = parseString(new_resource)
        new_resource: Element = new_resource.getElementsByTagName(
            'listaRecursos')
        if new_resource is None:
            return jsonify({'msg': 'El recurso no es válido'}), 400

        new_resource: List[Element] = new_resource[0].getElementsByTagName(
            'recurso')
        print(new_resource)
        quantity: int = create_elements(new_resource, store, 'listaRecursos')
        with open('store.xml', 'w') as file:
            store.writexml(file)

        return jsonify({'msg': f'{quantity} recursos creados'}), 200
    else:
        return jsonify({"msg": "Método no permitido"}), 405


@app.route('/crearCategoria', methods=['POST'])
def crearCategoria():
    if request.method == 'POST':
        new_category: str = request.data.decode('utf-8')
        new_category: Element = parseString(new_category)
        new_category: Element = new_category.getElementsByTagName(
            'listaCategorias')
        if new_category is None:
            return jsonify({'msg': 'La categoría no es válida'}), 400

        new_category: List[Element] = new_category[0].getElementsByTagName(
            'categoria')
        quantity: int = create_elements(new_category, store, 'listaCategorias')
        with open('store.xml', 'w') as file:
            store.writexml(file)

        return jsonify({'msg': f'{quantity} categorías creadas'}), 200


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


@app.route('/createConfig', methods=['POST'])
def createConfig():
    if request.method == 'POST':
        new_config: str = request.data.decode('utf-8')
        new_config: Element = parseString(new_config)
        new_config: Element = new_config.getElementsByTagName(
            'listaConfiguraciones')
        if new_config is None:
            return jsonify({'msg': 'La configuración no es válida'}), 400

        new_config: List[Element] = new_config[0].getElementsByTagName(
            'configuracion')
        quantity: int = create_elements(
            new_config, store, 'listaConfig')
        with open('store.xml', 'w') as file:
            store.writexml(file)

        return jsonify({'msg': f'{quantity} configuraciones creadas'}), 200

    return jsonify({'msg': 'No se pudo crear la configuración'}), 400


@app.route('/crearCliente', methods=['POST'])
def crearCliente():
    if request.method == 'POST':
        new_client: str = request.data.decode('utf-8')
        new_client: Element = parseString(new_client)
        new_client: List[Element] = new_client.getElementsByTagName(
            'cliente')
        quantity: int = create_clients(new_client, store)
        return jsonify({'msg': f'{quantity[0]} clientes creados y {quantity[1]} instancias'}), 200

    return jsonify({'msg': 'No se pudo crear el cliente'}), 400


@app.route('/crearInstancia', methods=['POST'])
def crearInstancia():
    if request.method == 'POST':
        new_instance: str = request.data.decode('utf-8')
        new_instance: Element = parseString(new_instance)
        new_instance: List[Element] = new_instance.getElementsByTagName(
            'instancia')
        quantity: int = create_elements(new_instance, store, 'listaInstancias')
        with open('store.xml', 'w') as file:
            store.writexml(file)

        return jsonify({'msg': f'{quantity} instancias creadas'}), 200


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
