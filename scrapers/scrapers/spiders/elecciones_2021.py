import os

import scrapy

from ..bajame_actas_2021 import get_session, get_locales, get_mesas, get_districts, \
    parse_acta_presidente, parse_acta_congreso, parse_acta_parlamento, save

BASE_URL = 'https://api.resultados.eleccionesgenerales2021.pe/'
HEADERS = {
    'Host': 'api.resultados.eleccionesgenerales2021.pe',
    'Origin': 'https://www.resultados.eleccionesgenerales2021.pe',
    'Referer': 'https://www.resultados.eleccionesgenerales2021.pe',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
}
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))


class Elecciones2021Spider(scrapy.Spider):
    name = "elecciones_2021"

    def start_requests(self):
        districts = get_districts()
        for district in districts:
            print(f'\tfetching district {district}')
            session = get_session()
            locales = get_locales(session, district.get('CDGO_DIST'))

            for local in locales:
                print(f'\tfetching local {local}')
                mesas = get_mesas(session, local)

                for mesa_number in mesas:
                    url = f'{BASE_URL}mesas/detalle/{mesa_number}'
                    yield scrapy.Request(
                        meta={'mesa': mesa_number},
                        url=url,
                        callback=self.parse,
                        headers=HEADERS,
                    )

    def parse(self, response):
        try:
            mesa_number = response.meta.get('mesa')
            res_json = response.json()
            acta_presidente = parse_acta_presidente(res_json)
            acta_congreso = parse_acta_congreso(res_json)
            acta_parlamento = parse_acta_parlamento(res_json)
            save(acta_presidente, mesa_number, 'presi')
            save(acta_congreso, mesa_number, 'congre')
            save(acta_parlamento, mesa_number, 'parla')
        except Exception:
            file_name = os.path.join(CURRENT_FOLDER, 'failed_to_fetch_mesas.jl')
            with open(file_name, 'a+') as handle:
                handle.write(f'{mesa_number}\n')
