import time

import requests as rqt

from services.logger import logger
from services.scraper import (
    check_if_are_new_apartments,
    get_recent_apartments,
    initialize_already_seen_file,
    update_most_recent_file,
)
from services.telegram import send_telegram_message

URLS = {
    "compra_providencia": {
        "chat_id": "-1002140402063",
        "url": "https://www.portalinmobiliario.com/venta/departamento/rm-metropolitana/providencia/pedro-de-valdivia-norte-o-barrio-italia-o-bellavista-o-los-leones-o-las-lilas-o-manuel-montt-o-metro-tobalaba---mall-costanera-o-pedro-de-valdivia-o-salvador/_OrderId_BEGINS*DESC_PriceRange_0CLF-11000CLF_BEDROOMS_3-*_NoIndex_True_TOTAL*AREA_100-*",
    },
    "compra_las_condes": {
        "chat_id": "-1002140402063",
        "url": "https://www.portalinmobiliario.com/venta/departamento/rm-metropolitana/las-condes/centro-financiero-o-barrio-el-golf-o-metro-escuela-militar-o-metro-manquehue---apumanque-o-parque-arauco/_OrderId_BEGINS*DESC_PriceRange_0CLF-11000CLF_BEDROOMS_3-*_COVERED*AREA_100-*_FULL*BATHROOMS_2-*_NoIndex_True",
    },
    "pillin": {
        "chat_id": "-4645606301",
        "url": "https://www.portalinmobiliario.com/arriendo/departamento/rm-metropolitana/nunoa/diagonal-oriente-o-juan-gomez-millas-o-metro-irarrazaval-o-metro-monsenor-eyzaguirre-o-metro-nunoa-o-parque-juan-xxiii-o-plaza-nunoa-o-villa-frei-o-villa-los-jardines---villa-los-presidentes/_OrderId_BEGINS*DESC_PriceRange_0CLP-700000CLP_BEDROOMS_*-3_FULL*BATHROOMS_*-2_NoIndex_True_TOTAL*AREA_60-100",
    },
}

if __name__ == "__main__":
    initialize_already_seen_file(URLS)

    while True:
        for key, commune in URLS.items():
            page_source = rqt.get(commune["url"]).text
            most_recent_apartments = get_recent_apartments(page_source, n_apartments=15)
            new_apartment_ids = check_if_are_new_apartments(key, most_recent_apartments)

            if len(new_apartment_ids) > 0:
                logger.info(f"Found {len(new_apartment_ids)} new apartments")
                new_apartments = {
                    id: most_recent_apartments[id]
                    for id in new_apartment_ids
                    if id in most_recent_apartments
                }

                for id, apartment in new_apartments.items():
                    logger.info(f"Sending message to Telegram for {apartment['title']}")
                    response = send_telegram_message(
                        apartment["url"], commune["chat_id"]
                    )
                    time.sleep(0.05)

                update_most_recent_file(key, new_apartments)
            else:
                logger.info("No new apartments found. Skipping...")

        time.sleep(60 * 60 * 2)
