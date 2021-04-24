from random import randint
from time import sleep
import requests
import json

from parsel import Selector

MAX_RETRIES = 5

BASE_URL = 'https://www.web.onpe.gob.pe/modElecciones/elecciones/elecciones2016/PRPCP2016/ajax.php'
DEPARTMENTS = [
    '010000',
    '020000',
    '030000',
    '040000',
    '050000',
    '060000',
    '240000',
    '070000',
    '080000',
    '090000',
    '100000',
    '110000',
    '120000',
    '130000',
    '140000',
    '150000',
    '160000',
    '170000',
    '180000',
    '190000',
    '200000',
    '210000',
    '220000',
    '230000',
    '250000',
]


def get_session():
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Origin': 'https://resultados.eleccionescongresales2020.pe',
        'X-Requested-With': 'XMLHttpRequest'
    })
    return s


def get_departments():
    session = get_session()
    payload = {
        'pid': '6233258373950512',
        '_clase': 'ubigeo',
        '_accion': 'getDepartamentos',
        'dep_id': '',
        'tipoElec': '10',
        'tipoC': '',
        'modElec': '',
        'ambito': 'P',
        'pantalla': ''
    }
    res = session.post(BASE_URL, data=payload)
    sel = Selector(res.text)
    departments = sel.xpath('//option/@value').extract()
    return extract_items(departments)


def extract_items(results):
    out = []
    for result in results:
        if result:
            out.append(result)
    return out


def get_provinces(department):
    session = get_session()
    payload = {
        'pid': '6233258373950512',
        '_clase': 'ubigeo',
        '_accion': 'getProvincias',
        'tipoElec': '10',
        'modElec': '',
        'dep_id': department,
        'pantalla': ''
    }
    res = session.post(BASE_URL, data=payload)
    sel = Selector(res.text)
    provinces = sel.xpath('//option/@value').extract()
    return extract_items(provinces)


def get_district(ubigeo):
    session = get_session()
    payload = {
        'pid': '6233258373950512',
        '_clase': 'ubigeo',
        '_accion': 'getDistritos',
        'prov_id': ubigeo,
        'tipoElec': '10',
        'modElec': '',
        'pantalla': ''
    }
    res = session.post(BASE_URL, data=payload)
    sel = Selector(res.text)
    districts = sel.xpath('//option/@value').extract()
    return extract_items(districts)


def download_district_result(ubigeo):
    """This is for president"""
    session = get_session()
    payload = {
        'pid': '6233258373950512',
        '_clase': 'resultado',
        '_accion': 'displayResultado',
        'tipoElec': '10',
        'modElec': 'PR',
        'ubigeo': ubigeo,
        'pantalla': '',
        'subpantalla': 'Datos',
    }
    res = session.post(BASE_URL, data=payload)
    sel = Selector(res.text)
    party_table = sel.xpath('//table[@class="table03"]')

    rows = party_table.xpath('.//tr')
    for row in rows:
        data = row.xpath('.//td/text()').extract()
        if data[0].startswith('ORGANIZACI'):
            continue





# ------------------

def do_get(url, retry=0):
    res = s.get(url)
    if res.status_code == 404:
        return None
    data = res.json()
    if not data:
        if retry > MAX_RETRIES:
            return None
        retry += 1
        sleep(1 * retry * retry)
        return do_get(url, retry)
    return data



def download_by_ids(all_ids):
    for i in all_ids:
        if i == 0:
            continue
        sleep(randint(0, 2))
        acta = f"{i}".zfill(6)
        url = f"{base_url}{acta}"
        print(acta)

        data = do_get(url)
        print(data)
        if not data:
            continue

        try:
            data_mesa = data["procesos"]["general"]["congresal"]
        except (KeyError, TypeError):
            continue
        votos = data["procesos"]["general"]["votos"]

        mesa_n = acta
        ubigeo = data_mesa["CCODI_UBIGEO"]
        departamento = data_mesa["DEPARTAMENTO"]
        provincia = data_mesa["PROVINCIA"]
        distrito = data_mesa["DISTRITO"]
        estado_proceso = data["procesos"]["general"]["congresal"]["OBSERVACION"]

        item = dict()
        item["mesa_numero"] = mesa_n
        item["ubigeo"] = ubigeo
        item["departamento"] = departamento
        item["provincia"] = provincia
        item["distrito"] = distrito
        item["estado_proceso"] = estado_proceso

        for voto in votos:
            if voto["AUTORIDAD"] in ["TOTAL VOTOS EMITIDOS", "VOTOS IMPUGNADOS",
                                     "VOTOS NULOS", "VOTOS EN BLANCO", "TOTAL VOTOS VALIDOS"]:
                continue
            item["org_politica"] = voto["AUTORIDAD"]
            item["total_votos"] = voto["congresal"]

            with open("missing.json", "a") as handle:
                handle.write(json.dumps(item) + "\n")

# all_ids = list(range(901850, 910000))
# download_by_ids(all_ids)


if __name__ == "__main__":
    get_departments()
