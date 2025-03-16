import time

import requests as rqt

from services.logger import logger
from services.scraper import (
    check_if_are_new_apartments,
    get_recent_apartments,
    update_most_recent_file,
)
from services.telegram import send_telegram_message

URLS = [
    "https://www.portalinmobiliario.com/venta/departamento/providencia-metropolitana/_OrderId_BEGINS*DESC_PriceRange_6000CLF-11000CLF_BEDROOMS_3-*_NoIndex_True_TOTAL*AREA_100-*#applied_filter_id%3Dprice%26applied_filter_name%3DPrecio%26applied_filter_order%3D6%26applied_value_id%3D6000-11000%26applied_value_name%3DCLF6000-CLF11000%26applied_value_order%3D4%26applied_value_results%3DUNKNOWN_RESULTS%26is_custom%3Dtrue",
    "https://www.portalinmobiliario.com/venta/departamento/las-condes-metropolitana/_OrderId_BEGINS*DESC_PriceRange_6000CLF-11000CLF_BEDROOMS_3-*_COVERED*AREA_100-*_FULL*BATHROOMS_2-*",
]

if __name__ == "__main__":
    while True:
        for url in URLS:
            page_source = rqt.get(url).text
            most_recent_apartments = get_recent_apartments(page_source, n_apartments=15)
            new_apartments = check_if_are_new_apartments(most_recent_apartments)

            logger.info(f"Found {len(new_apartments)} new apartments")

            if new_apartments:
                for title, url in new_apartments:
                    logger.info(f"Sending message to Telegram for {title}")
                    response = send_telegram_message(url)
                update_most_recent_file(most_recent_apartments)

        time.sleep(60 * 60 * 2)
