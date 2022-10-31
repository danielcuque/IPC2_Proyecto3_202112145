from xml.dom.minicompat import NodeList
from werkzeug.datastructures import FileStorage
from typing import List
from xml.dom.minidom import Element, parse, parseString


ALLOWED_EXTENSIONS = set(['txt', 'xml', 'json'])


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def read_info(file: FileStorage) -> str:
    information_file: str = file.stream.read().decode('utf-8')
    config_info: Element = parseString(information_file)

    store: Element = parse('store.xml')

    client_list: Element = config_info.getElementsByTagName('cliente')
    resources_list: Element = config_info.getElementsByTagName('recurso')
    categories_list: Element = config_info.getElementsByTagName('categoria')

    clients_created: int = create_elements(client_list, store, 'listaClientes')
    resources_created: int = create_elements(
        resources_list, store, 'listaRecursos')
    categories_created: int = create_elements(
        categories_list, store, 'listaCategorias')

    return f'Se crearon {clients_created} clientes, {resources_created} recursos, y {categories_created} categorias'


def create_elements(elements: List[Element], store: Element, name_list: str) -> int:
    count: int = 0
    list_to_insert: NodeList = store.getElementsByTagName(name_list)
    print(list_to_insert)
    for element in elements:
        count += 1
        list_to_insert.append(element)

    store.writexml('store.xml')
    return count
