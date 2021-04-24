import csv
from random import randint
from time import sleep
import requests
import json

MAX_RETRIES = 5

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

base_url = "https://2601202919738512020.eleccionescongresales2020.pe/v1/ECE2020/mesas/detalle/"

s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'Origin': 'https://resultados.eleccionescongresales2020.pe',
    'X-Requested-With': 'XMLHttpRequest'
})

def download_by_ids(all_ids):
    for i in all_ids:
        if i == 0:
            continue
        sleep(randint(0, 2))
        acta = f"{i}".zfill(6)
        url = f"{base_url}{acta}"
        print(acta)

        data = do_get(url)
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


all_ids = set()
crawled_actas = set()

with open('complete.json', 'r') as handle:
    for line in handle:
        line = line.strip()
        line = json.loads(line)
        acta = int(line['mesa_numero'])
        crawled_actas.add(acta)

with open('missing.json', 'r') as handle:
    for line in handle:
        line = line.strip()
        line = json.loads(line)
        acta = int(line['mesa_numero'])
        crawled_actas.add(acta)

with open('mesas_faltantes.csv', 'r') as handle:
    for line in handle:
        line = line.strip()
        acta = int(line)
        if acta not in crawled_actas:
            all_ids.add(acta)

download_by_ids(list(all_ids))
