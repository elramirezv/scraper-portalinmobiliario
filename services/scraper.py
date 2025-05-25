import json
import re

from bs4 import BeautifulSoup


def initialize_already_seen_file(urls):
    """Initializes the already_seen.json file with empty dictionaries for each URL key.

    Args:
        urls (dict): Dictionary with keys to initialize in the JSON file
    """
    try:
        # Try to read the existing file
        with open("already_seen.json", "r", encoding="utf8") as json_file:
            already_seen = json.load(json_file)

    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is invalid, start with empty dict
        already_seen = {}

    # Add any missing keys with empty lists
    for key in urls:
        if key not in already_seen:
            already_seen[key] = {}

    # Write back to the file
    with open("already_seen.json", "w", encoding="utf8") as json_file:
        json.dump(already_seen, json_file, indent=4, ensure_ascii=False)


def check_if_are_new_apartments(key, most_recent_ids):
    """Revisa si es que hay nuevos departamentos de acuerdo a lo que está previamente
    guardado en el archivo JSON.

    Args:
        key (str): La clave del diccionario en el JSON (ej: "compra_providencia")
        most_recent_ids (list): Lista de ids de posibles nuevos departamentos

    Returns:
        list: Lista de nuevos IDs (title, url)
    """
    with open("already_seen.json", "r", encoding="utf8") as jfile:
        existing_data = json.load(jfile)[key]
        return list(filter(lambda x: x not in existing_data, most_recent_ids))


def update_most_recent_file(key, new_apartments):
    """Actualiza el archivo JSON de los departamentos que ya fueron notificados

    Args:
        key (str): La clave del diccionario en el JSON (ej: "compra_providencia")
        most_recent_titles (list): Lista de tuplas (title, url)
    """
    with open("already_seen.json", "r", encoding="utf8") as json_file_read:
        already_seen = json.load(json_file_read)

    for id, apartment_info in new_apartments.items():
        already_seen[key][id] = apartment_info

    with open("already_seen.json", mode="w", encoding="utf8") as jfile:
        json.dump(already_seen, jfile, indent=4, ensure_ascii=False)


def get_recent_apartments(page, n_apartments=15):
    """Obtiene los últimos N departamentos.

    Args:
        page (string): HTML de la página del portal inmobiliario
        n_apartments (int, optional): Número de departamentos a obtener. Defaults to 15.

    Returns:
        dict: Diccionario con los IDs como keys y los valores son los titulos y urls
    """
    soup = BeautifulSoup(page, "html.parser")
    items = soup.find_all("li", class_="ui-search-layout__item", limit=n_apartments)
    apartments = {}
    for item in items:
        component = item.find("a", class_="poly-component__title")
        title = component.text.strip()
        url = component.attrs["href"].split("#")[0]
        id = extract_id(url)
        apartments[id] = {"title": title, "url": url}
    return apartments


def extract_id(url):
    """
    Extract the ID from a Portal Inmobiliario URL.

    Args:
        url (str): The URL from Portal Inmobiliario

    Returns:
        str: The ID number that comes after MLC-

    Example:
        >>> url = "https://portalinmobiliario.com/MLC-2901781622-precioso-depto-3d2b-2estacbod-en-providencia-_JM"
        >>> extract_id(url)
        '2901781622'
    """
    pattern = r"MLC-(\d+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None
