import re
import copy
from werkzeug.datastructures import FileStorage
from typing import List
from xml.dom.minidom import Element, parse, parseString
from datetime import datetime


ALLOWED_EXTENSIONS = set(['txt', 'xml', 'json'])

date = re.compile(
    r"[a-zA-Z ;,]*(\d{2}:\d{2})*[a-zA-Z ,;]*(\d{2}/\d{2}/\d{4})+[a-zA-Z ;,]*(\d{2}:\d{2})*[a-zA-Z ;,]*")


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_clients(clients: List[Element], store: Element) -> List[int]:
    clients_created: int = 0
    instances_created: int = 0

    # Get the lists of clients and instances for the store
    list_to_insert: Element = store.getElementsByTagName('listaClientes')[0]
    instances_list: Element = store.getElementsByTagName('listInstances')[0]

    # Iterate each client
    for client in clients:

        # Get the instances of the client
        instances: List[Element] = client.getElementsByTagName(
            'listaInstancias')[0].getElementsByTagName('instancia')

        for instance in instances:
            instance_initial_date: str = instance.getElementsByTagName('fechaInicio')[
                0].firstChild.data

            util_initial_date: str = format_date(instance_initial_date)
            if util_initial_date != '':
                instance.getElementsByTagName('fechaInicio')[
                    0].firstChild.nodeValue = util_initial_date

            instance_final_date = instance.getElementsByTagName(
                'fechaFinal')
            instance_final_date = instance_final_date[0].firstChild
            if instance_final_date is not None:
                util_final_date: str = format_date(instance_final_date.data)
                if util_final_date != '':
                    instance.getElementsByTagName('fechaFinal')[
                        0].firstChild.nodeValue = util_final_date

        instances: List[Element] = copy.deepcopy(
            instances)

        # Iterate each instance
        for instance in instances:
            instances_created += 1
            instances_list.appendChild(instance)

        clients_created += 1
        list_to_insert.appendChild(client)

    with open('store.xml', 'w') as file:
        store.writexml(file)
    return [clients_created, instances_created]


def format_date(original_date: str) -> str:
    days_format_date: str = date.match(original_date).group(2)
    hours_format_date1: str = date.match(original_date).group(1)
    hours_format_date2: str = date.match(original_date).group(3)
    util_initial_date: str = ""
    if days_format_date is not None:
        if hours_format_date1 is not None:
            util_initial_date = f'{days_format_date} {hours_format_date1}'
        elif hours_format_date2 is not None:
            util_initial_date = f'{days_format_date} {hours_format_date2}'
        else:
            util_initial_date = days_format_date

    return util_initial_date


def create_elements(elements: List[Element], store: Element, name_list: str) -> int:
    count: int = 0
    list_to_insert: Element = store.getElementsByTagName(name_list)[0]

    if name_list == 'listaCategorias':
        list_of_config: Element = store.getElementsByTagName('listaConfig')[
            0]

    for element in elements:
        count += 1
        list_to_insert.appendChild(element)

        if name_list == 'listInstances':
            instance_initial_date: str = element.getElementsByTagName('fechaInicio')[
                0].firstChild.data

            util_initial_date: str = format_date(instance_initial_date)
            if util_initial_date != '':
                element.getElementsByTagName('fechaInicio')[
                    0].firstChild.nodeValue = util_initial_date

            instance_final_date = element.getElementsByTagName(
                'fechaFinal')
            instance_final_date = instance_final_date[0].firstChild
            if instance_final_date is not None:
                util_final_date: str = format_date(instance_final_date.data)
                if util_final_date != '':
                    element.getElementsByTagName('fechaFinal')[
                        0].firstChild.nodeValue = util_final_date

        if name_list == 'listaCategorias':
            configs: List[Element] = copy.deepcopy(
                element.getElementsByTagName('listaConfiguraciones')[0].getElementsByTagName('configuracion'))

            for config in configs:
                list_of_config.appendChild(config)
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


def cancel_instance(instance_id: str, store: Element) -> int:
    instances_list: List[Element] = store.getElementsByTagName('instancia')
    count = 0

    for instance in instances_list:
        if instance.getAttribute('id') == instance_id:
            instance.getElementsByTagName(
                'estado')[0].firstChild.nodeValue = 'Cancelada'
            instance.getElementsByTagName(
                'fechaFinal')[0].appendChild(store.createTextNode(str(datetime.now().strftime('%d/%m/%Y %H:%M'))))
            count += 1
    with open('store.xml', 'w') as file:
        store.writexml(file)
    return count
