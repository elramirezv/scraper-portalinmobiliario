import json

from bs4 import BeautifulSoup


def check_if_are_new_apartments(most_recent_titles):
    """Revisa si es que hay nuevos departamentos de acuerdo a lo que está previamente
    guardado en el archivo JSON.
    Retorna los que no se encuentran guardados en el JSON

    Args:
        most_recent_titles (list): Lista de posibles nuevos departamentos

    Returns:
        list: Lista de nuevos departamentos
    """
    with open("already_seen.json", "r", encoding="utf8") as jfile:
        titles_list = json.load(jfile)
        titles_already_seen = {line.strip().split("|||")[0] for line in titles_list}
        return [
            item for item in most_recent_titles if item[0] not in titles_already_seen
        ]


def update_most_recent_file(most_recent_titles):
    """Actualiza el archivo JSON de los departamentos que ya fueron notificados

    Args:
        most_recent_titles (list)
    """
    with open("already_seen.json", "r", encoding="utf8") as json_file_read:
        titles_already_seen = set(json.load(json_file_read))

    new_titles = {f"{title}|||{url}" for title, url in most_recent_titles}
    titles_already_seen.update(new_titles)

    with open("already_seen.json", mode="w", encoding="utf8") as jfile:
        json.dump(list(titles_already_seen), jfile, indent=4, ensure_ascii=False)


def get_recent_apartments(page, n_apartments=15):
    """Obtiene los últimos N departamentos.

    Args:
        page (string): HTML de la página del portal inmobiliario
        n_apartments (int, optional): [description]. Defaults to 15.

    Returns:
        list(list)
    """
    soup = BeautifulSoup(page, "html.parser")
    items = soup.find_all("li", class_="ui-search-layout__item", limit=n_apartments)
    apartments = []
    for item in items:
        component = item.find("a", class_="poly-component__title")
        title = component.text
        link = component.attrs["href"].split("#")[0]
        apartments.append([title, link])
    return apartments
