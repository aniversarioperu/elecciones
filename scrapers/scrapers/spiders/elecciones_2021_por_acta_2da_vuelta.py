import json
import os

import scrapy

from ..bajame_actas_2021 import save

BASE_URL = 'https://api.resultadossep.eleccionesgenerales2021.pe/mesas/detalle/'
# 'https://api.resultadossep.eleccionesgenerales2021.pe/mesas/detalle/000001?name=param'

HEADERS = {
    'Authority': 'api.resultadossep.eleccionesgenerales2021.pe',
    'Origin': 'https://www.resultadossep.eleccionesgenerales2021.pe',
    'Referer': 'https://www.resultadossep.eleccionesgenerales2021.pe/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
}
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))


class Elecciones2021PorActa2daVueltaSpider(scrapy.Spider):
    """Descarga resultados for acta"""
    name = "elecciones_2021_por_acta_2da_vuelta"

    def start_requests(self):
        try:
            with open(os.path.join(CURRENT_FOLDER, 'presi_2021_2nda_vuelta.jl')) as handle:
                current_scrape = handle.readlines()
        except FileNotFoundError:
            current_scrape = []
            pass

        mesas_already_scraped = set()
        for i in current_scrape:
            json.loads(i)
            mesas_already_scraped.add(i['mesa'])
        print(f'mesas scrapped {mesas_already_scraped}')

        # Mesas escrapeadas en ateriores procesos
        mesas_anteriores = []
        with open(os.path.join(CURRENT_FOLDER, 'acta_numeros.txt')) as handle:
            for i in handle.readlines():
                i = i.strip()
                mesas_anteriores.append(i)

        for mesa_number in mesas_anteriores:
            if mesa_number not in mesas_already_scraped:
                yield scrapy.Request(
                    meta={'mesa': mesa_number},
                    url=f'{BASE_URL}{mesa_number}',
                    callback=self.parse,
                    headers=HEADERS,
                )

        for i in range(1, 999999):
            i = str(i)
            mesa_number = i.zfill(6)
            if mesa_number not in mesas_already_scraped and mesa_number not in mesa_number:
                yield scrapy.Request(
                    meta={'mesa': mesa_number},
                    url=f'{BASE_URL}{mesa_number}',
                    callback=self.parse,
                    headers=HEADERS,
                )
            if int(i) > 5:
                break

    def parse(self, response):
        mesa_number = response.meta.get('mesa')
        try:
            self.parse_response(response)
        except Exception as error:
            file_name = os.path.join(CURRENT_FOLDER, 'failed_to_fetch_mesas.jl')
            with open(file_name, 'a+') as handle:
                handle.write(f'{mesa_number}\n')

    def parse_response(self, response):
        mesa_number = response.meta.get('mesa')
        res_json = json.loads(response.text)
        res_json['mesa'] = mesa_number
        if 'generalPre' in res_json['procesos']:
            save(res_json, mesa_number, 'presi_2021_2nda_vuelta')
