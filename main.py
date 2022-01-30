import os
from bs4 import BeautifulSoup
import requests as rqt
import json
from dotenv import load_dotenv

load_dotenv()

# URL a las comunas que queremos consultar
LAS_CONDES_URL = 'https://www.portalinmobiliario.com/arriendo/departamento/las-condes-metropolitana/_OrderId_BEGINS*DESC_PriceRange_500000CLP-800000CLP_BEDROOMS_2-*_COVERED*AREA_70-*_NoIndex_True#applied_filter_id%3Dprice%26applied_filter_name%3DPrecio%26applied_filter_order%3D4%26applied_value_id%3D500000-800000%26applied_value_name%3DCLP500000-CLP800000%26applied_value_order%3D4%26applied_value_results%3DUNKNOWN_RESULTS%26is_custom%3Dtrue'
PROVIDENCIA_URL = 'https://www.portalinmobiliario.com/arriendo/departamento/providencia-metropolitana/_OrderId_BEGINS*DESC_PriceRange_500000CLP-800000CLP_BEDROOMS_2-*_COVERED*AREA_70-*_NoIndex_True#applied_filter_id%3Dprice%26applied_filter_name%3DPrecio%26applied_filter_order%3D3%26applied_value_id%3D500000-800000%26applied_value_name%3DCLP500000-CLP800000%26applied_value_order%3D4%26applied_value_results%3DUNKNOWN_RESULTS%26is_custom%3Dtrue'
NUNOA_URL = 'https://www.portalinmobiliario.com/arriendo/departamento/nunoa-metropolitana/_OrderId_BEGINS*DESC_PriceRange_500000CLP-800000CLP_BEDROOMS_2-*_COVERED*AREA_70-*_NoIndex_True#applied_filter_id%3Dprice%26applied_filter_name%3DPrecio%26applied_filter_order%3D3%26applied_value_id%3D500000-800000%26applied_value_name%3DCLP500000-CLP800000%26applied_value_order%3D4%26applied_value_results%3DUNKNOWN_RESULTS%26is_custom%3Dtrue'

COMMUNES = [
    {
        'name': 'las_condes',
        'link': LAS_CONDES_URL
    },
    {
        'name': 'nunoa',
        'link': NUNOA_URL
    },
    {
        'name': 'providencia',
        'link': PROVIDENCIA_URL
    }
]

def check_if_are_new_apartments(commune, most_recent_titles):
    """Revisa si es que hay nuevos departamentos de acuerdo a lo que está previamente
    guardado en el archivo JSON.
    Retorna los que no se encuentran guardados en el JSON

    Args:
        commune (string)
        most_recent_titles (list): Lista de posibles nuevos departamentos

    Returns:
        list: Lista
    """
    with open('already_seen.json', 'r', encoding='utf8') as jfile:
        titles_list = json.load(jfile)[commune]
        titles_already_seen = [line.strip().split('|||')[0] for line in titles_list]
        list_difference = [item for item in most_recent_titles if item[0]
                           not in titles_already_seen]
        return list_difference

def update_most_recent_file(commune, most_recent_titles):
    """Actualiza el archivo JSON de los departamentos que ya fueron notificados

    Args:
        commune (string)
        most_recent_titles (list)
    """
    json_file_read = open('already_seen.json', 'r', encoding='utf8')
    titles_already_seen = json.load(json_file_read)
    json_file_read.close()
    most_recent_titles_list = [f'{title}|||{url}' for title, url in most_recent_titles]
    titles_already_seen[commune] = most_recent_titles_list
    with open('already_seen.json', mode='w', encoding='utf8') as jfile:
        json.dump(titles_already_seen, jfile, indent=4, ensure_ascii=False)

def get_recent_apartments(page, n_apartments=15):
    """Obtiene los últimos N departamentos.

    Args:
        page (string): HTML de la página del portal inmobiliario
        n_apartments (int, optional): [description]. Defaults to 15.

    Returns:
        list(list)
    """
    soup = BeautifulSoup(page, 'html.parser')
    items = soup.find_all("li", class_="ui-search-layout__item", limit=n_apartments)
    apartments = []
    for item in items:
        title = item.find('p', class_='ui-search-item__group__element').string
        link = item.find('a', class_='ui-search-link').attrs['href']
        link = link.split('#')[0] # Nos quedamos con la primera parte del link
        apartments.append([title, link])
    return apartments


if __name__ == "__main__":
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    for commune in COMMUNES:
        page_source = rqt.get(commune['link']).text
        most_recent_apartments = get_recent_apartments(page_source)
        new_apartments = check_if_are_new_apartments(commune['name'], most_recent_apartments)
        if len(new_apartments) > 0:
            # Notificamos a un URL los nuevos departamentos, puede ser una integración con Slack o Discord
            rqt.post(WEBHOOK_URL, json={'data': new_apartments})
            # Actualizamos el archivo JSON para no volver a notificar
            update_most_recent_file(commune['name'], most_recent_apartments)
