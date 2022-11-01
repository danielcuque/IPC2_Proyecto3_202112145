import re
from werkzeug.datastructures import FileStorage
from typing import List
from xml.dom.minidom import Element, parse, parseString


ALLOWED_EXTENSIONS = set(['txt', 'xml', 'json'])

date = re.compile(r'.*(\d{2}:\d{2})*.*(\d{2}/\d{2}/\d{4})+.*(\d{2}:\d{2})*.*')


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_clients(clients: List[Element], store: Element) -> List[int]:
    clients_created: int = 0
    instances_created: int = 0
    list_to_insert: Element = store.getElementsByTagName('listaClientes')[0]
    for client in clients:
        clients_created += 1
        list_to_insert.appendChild(client)
        instances_created += len(client.getElementsByTagName('instancia'))

    with open('store.xml', 'w') as file:
        store.writexml(file)
    return [clients_created, instances_created]


def create_elements(elements: List[Element], store: Element, name_list: str) -> int:
    count: int = 0
    list_to_insert: Element = store.getElementsByTagName(name_list)[0]
    for element in elements:
        count += 1
        list_to_insert.appendChild(element)
    return count


def read_info(file: FileStorage) -> List[int]:
    information_file: str = file.stream.read().decode('utf-8')
    config_info: Element = parseString(information_file)

    store: Element = parse('store.xml')

    client_list: List[Element] = config_info.getElementsByTagName('cliente')
    resources_list: List[Element] = config_info.getElementsByTagName(
        'listaRecursos')[0].getElementsByTagName('recurso')
    categories_list: List[Element] = config_info.getElementsByTagName(
        'categoria')

    resources_created: int = create_elements(
        resources_list, store, 'listaRecursos')

    categories_created: int = create_elements(
        categories_list, store, 'listaCategorias')

    instances_and_clients: List[int] = create_clients(client_list, store)

    return [resources_created, categories_created] + instances_and_clients
