import json
import os

import scrapy

from ..bajame_actas_2021 import save

BASE_URL = 'https://www.web.onpe.gob.pe/modElecciones/elecciones/elecciones2016/PRPCP2016/ajax.php'
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


class Elecciones2016PorActaSpider(scrapy.Spider):
    """Descarga resultados for acta"""
    name = "elecciones_2016_por_acta"

    def start_requests(self):
        try:
            with open(os.path.join(CURRENT_FOLDER, 'presi_2016.jl')) as handle:
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
            if mesa_number not in mesas:
                yield scrapy.FormRequest(
                    meta={'mesa': mesa_number},
                    formdata={
                        'pid': '7581594407589587',
                        '_clase': "mesas",
                        '_accion': 'displayMesas',
                        'nroMesa': mesa_number,
                        'pornumero': '1',
                        'tipoElec': '10',
                        'boopornumero': '1',
                    },
                    url=BASE_URL,
                    callback=self.parse,
                    headers=HEADERS,
                )

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
        acta = {
            'acta_numero': mesa_number,
            'votos': [],
        }

        departamento, provincia, distrito, local, direccion = response.xpath(
            '//table[@class="table14"]//tr[2]//td/text()'
        ).extract()
        acta['departamento'] = departamento
        acta['provincia'] = provincia
        acta['distrito'] = distrito
        acta['local'] = local
        acta['direccion'] = direccion

        electores_habiles, total_votantes, estado_acta = response.xpath(
            '//table[@class="table15"]//tr[2]//td/text()'
        ).extract()
        estado_acta = estado_acta.strip()

        acta['electores_habiles'] = electores_habiles
        acta['total_votantes'] = total_votantes
        acta['estado_acta'] = estado_acta
        acta['votacion_partidos'] = []

        rows = response.xpath('//table[@class="table06"]/tbody/tr')

        for row in rows:
            if row.xpath('@class').extract_first():
                continue

            partido = row.xpath('.//td[1]/text()').extract_first()
            if not partido:
                continue

            if not partido.startswith('VOTOS') and not partido.startswith('TOTAL'):
                votos_partido = row.xpath('.//td[3]/text()').extract_first() or ''
                votos_partido = votos_partido.strip()
                acta['votos'].append({partido: votos_partido})
            elif partido.startswith('VOTOS') and 'BLANCO' in partido:
                votos_blanco = row.xpath('.//td[2]/text()').extract_first() or ''
                votos_blanco = votos_blanco.strip()
            elif partido.startswith('VOTOS') and 'NULOS' in partido:
                votos_nulo = row.xpath('.//td[2]/text()').extract_first() or ''
                votos_nulo = votos_nulo.strip()
            elif partido.startswith('VOTOS') and 'IMPUGNADOS' in partido:
                votos_impugnados = row.xpath('.//td[2]/text()').extract_first() or ''
                votos_impugnados = votos_impugnados.strip()
            elif partido.startswith('TOTAL'):
                votos_total = row.xpath('.//td[2]/text()').extract_first() or ''
                votos_total = votos_total.strip()

        acta['votos_blanco'] = votos_blanco
        acta['votos_nulo'] = votos_nulo
        acta['votos_impugnados'] = votos_impugnados
        acta['votos_total'] = votos_total

        save(acta, mesa_number, 'presi_2016')
