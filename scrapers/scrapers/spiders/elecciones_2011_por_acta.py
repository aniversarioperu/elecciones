import json
import os

import scrapy

from ..bajame_actas_2021 import save

BASE_URL = 'https://www.web.onpe.gob.pe/modElecciones/elecciones/elecciones2011/1ravuelta/onpe/presidente/rep_mesas_det_pre.php?cnume_acta='
HEADERS = {
    'Host': 'www.web.onpe.gob.pe',
    'Origin': 'https://www.web.onpe.gob.pe',
    'Referer': 'https://www.web.onpe.gob.pe/modElecciones/elecciones/elecciones2016/PRPCP2016/Actas-por-numero.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
    "Cookie": "ga=GA1.3.70616642.1618175520; PHPSESSID=bkpu5fej64f2dt4vikelg2kmk7; TS01119a09=0123114e419e6bcd65ba979a78ceb5ad8f101d440d7b611dd1fb280537ec06c79fae8d84c10d8a948a217cbdd25bb1c098ecbc782b113ff4fc2ec5e745b30f70119360e5a2; web_server_iron=!iFSl8oWL2D24BKirtEYETGl+f9BADawu6KPeh2FekCd22upmkm3DLZ+qV3aQe5YxPweVcoVXgAqgS8c=",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
}
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))


class Elecciones2011PorActaSpider(scrapy.Spider):
    """Descarga resultados for acta"""
    name = "elecciones_2011_por_acta"

    def start_requests(self):
        try:
            with open(os.path.join(CURRENT_FOLDER, 'presi_2011.jl')) as handle:
                data = handle.readlines()
        except FileNotFoundError:
            data = []
            pass

        mesas = set()
        for i in data:
            json.loads(i)
            mesas.add(i['mesa'])

        for i in range(1, 999999):
            i = str(i)
            mesa_number = i.zfill(6)
            url = BASE_URL + mesa_number
            if mesa_number not in mesas:
                yield scrapy.Request(
                    meta={'mesa': mesa_number},
                    url=url,
                    callback=self.parse,
                    headers=HEADERS,
                )

    def parse(self, response):
        print(response)
        mesa_number = response.meta.get('mesa')
        try:
            self.parse_response(response)
        except Exception as error:
            file_name = os.path.join(CURRENT_FOLDER, 'failed_to_fetch_mesas.jl')
            with open(file_name, 'a+') as handle:
                handle.write(f'{mesa_number}\n')

    def parse_response(self, response):
        mesa_number = response.meta.get('mesa')
        acta = {
            'acta_numero': mesa_number,
            'votos': [],
        }

        acta['departamento'] = response.xpath('//table[2]/tr[4]/td[4]/text()').extract_first()
        acta['provincia'] = response.xpath('//table[2]/tr[5]/td[4]/text()').extract_first()
        acta['distrito'] = response.xpath('//table[2]/tr[6]/td[4]/text()').extract_first()
        acta['local'] = response.xpath('//table[2]/tr[7]/td[4]/text()').extract_first()
        acta['direccion'] = response.xpath('//table[2]/tr[8]/td[4]/text()').extract_first()

        acta['electores_habiles'] = response.xpath('//table[2]/tr[10]/td[4]/text()').extract_first()
        acta['total_votantes'] = response.xpath('//table[2]/tr[11]/td[4]/text()').extract_first()
        acta['estado_acta'] = response.xpath('//table[2]/tr[12]/td[4]/text()').extract_first()
        acta['votacion_partidos'] = []

        rows = response.xpath('//table[3]/tr')

        for row in rows:
            if row.xpath('@height="40"').extract_first() == '1':
                partido_name = row.xpath('td[1]/span/text()').extract_first()
                if partido_name:
                    voto = row.xpath('td[3]/span/text()').extract_first()
                    if not voto:
                        voto = '0'
                    acta['votos'].append({partido_name: voto})
            else:
                row_name = row.xpath('td[1]/span/text()').extract_first()
                if row_name and 'Blancos' in row_name:
                    acta['votos_blanco'] = row.xpath('td[2]/span/text()').extract_first() or '0'
                elif row_name and 'Nulos' in row_name:
                    acta['votos_nulo'] = row.xpath('td[2]/span/text()').extract_first() or '0'
                elif row_name and 'Impugnados' in row_name:
                    acta['votos_impugnados'] = row.xpath('td[2]/span/text()').extract_first() or '0'
                elif row_name and 'Total' in row_name:
                    acta['votos_total'] = row.xpath('td[2]/span/text()').extract_first() or '0'

        save(acta, mesa_number, 'presi_2011')
