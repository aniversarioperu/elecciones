from random import randint
from time import sleep
import requests
import json
import os


MAX_RETRIES = 5

BASE_URL = 'https://api.resultados.eleccionesgenerales2021.pe/'
HEADERS = {
    'Host': 'api.resultados.eleccionesgenerales2021.pe',
    'Origin': 'https://www.resultados.eleccionesgenerales2021.pe',
    'Referer': 'https://www.resultados.eleccionesgenerales2021.pe',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
}
DEPARTMENTS = [
    {'CDGO_DEP': '010000', 'DESC_DEP': 'AMAZONAS', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '020000', 'DESC_DEP': 'ANCASH', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '030000', 'DESC_DEP': 'APURIMAC', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '040000', 'DESC_DEP': 'AREQUIPA', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '050000', 'DESC_DEP': 'AYACUCHO', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '060000', 'DESC_DEP': 'CAJAMARCA', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '240000', 'DESC_DEP': 'CALLAO', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '070000', 'DESC_DEP': 'CUSCO', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '080000', 'DESC_DEP': 'HUANCAVELICA', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '090000', 'DESC_DEP': 'HUANUCO', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '100000', 'DESC_DEP': 'ICA', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '110000', 'DESC_DEP': 'JUNIN', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '120000', 'DESC_DEP': 'LA LIBERTAD', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '130000', 'DESC_DEP': 'LAMBAYEQUE', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '140000', 'DESC_DEP': 'LIMA', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '150000', 'DESC_DEP': 'LORETO', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '160000', 'DESC_DEP': 'MADRE DE DIOS', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '170000', 'DESC_DEP': 'MOQUEGUA', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '180000', 'DESC_DEP': 'PASCO', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '190000', 'DESC_DEP': 'PIURA', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '200000', 'DESC_DEP': 'PUNO', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '210000', 'DESC_DEP': 'SAN MARTIN', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '220000', 'DESC_DEP': 'TACNA', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '230000', 'DESC_DEP': 'TUMBES', 'CDGO_PADRE': '000000'},
    {'CDGO_DEP': '250000', 'DESC_DEP': 'UCAYALI', 'CDGO_PADRE': '000000'},
]
PROVINCES = [
    {'CDGO_PROV': '030100', 'DESC_PROV': 'ABANCAY', 'CDGO_PADRE': '030000'},
    {'CDGO_PROV': '080200', 'DESC_PROV': 'ACOBAMBA', 'CDGO_PADRE': '080000'},
    {'CDGO_PROV': '070200', 'DESC_PROV': 'ACOMAYO', 'CDGO_PADRE': '070000'},
    {'CDGO_PROV': '020200', 'DESC_PROV': 'AIJA', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '150200', 'DESC_PROV': 'ALTO AMAZONAS', 'CDGO_PADRE': '150000'},
    {'CDGO_PROV': '090200', 'DESC_PROV': 'AMBO', 'CDGO_PADRE': '090000'},
    {'CDGO_PROV': '030300', 'DESC_PROV': 'ANDAHUAYLAS', 'CDGO_PADRE': '030000'},
    {'CDGO_PROV': '080300', 'DESC_PROV': 'ANGARAES', 'CDGO_PADRE': '080000'},
    {'CDGO_PROV': '070300', 'DESC_PROV': 'ANTA', 'CDGO_PADRE': '070000'},
    {'CDGO_PROV': '030400', 'DESC_PROV': 'ANTABAMBA', 'CDGO_PADRE': '030000'},
    {'CDGO_PROV': '021600', 'DESC_PROV': 'ANTONIO RAIMONDI', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '040100', 'DESC_PROV': 'AREQUIPA', 'CDGO_PADRE': '040000'},
    {'CDGO_PROV': '120800', 'DESC_PROV': 'ASCOPE', 'CDGO_PADRE': '120000'},
    {'CDGO_PROV': '021800', 'DESC_PROV': 'ASUNCION', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '250300', 'DESC_PROV': 'ATALAYA', 'CDGO_PADRE': '250000'},
    {'CDGO_PROV': '190200', 'DESC_PROV': 'AYABACA', 'CDGO_PADRE': '190000'},
    {'CDGO_PROV': '030200', 'DESC_PROV': 'AYMARAES', 'CDGO_PADRE': '030000'},
    {'CDGO_PROV': '200200', 'DESC_PROV': 'AZANGARO', 'CDGO_PADRE': '200000'},
    {'CDGO_PROV': '010200', 'DESC_PROV': 'BAGUA', 'CDGO_PADRE': '010000'},
    {'CDGO_PROV': '140900', 'DESC_PROV': 'BARRANCA', 'CDGO_PADRE': '140000'},
    {'CDGO_PROV': '210700', 'DESC_PROV': 'BELLAVISTA', 'CDGO_PADRE': '210000'},
    {'CDGO_PROV': '120200', 'DESC_PROV': 'BOLIVAR', 'CDGO_PADRE': '120000'},
    {'CDGO_PROV': '020300', 'DESC_PROV': 'BOLOGNESI', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '010300', 'DESC_PROV': 'BONGARA', 'CDGO_PADRE': '010000'},
    {'CDGO_PROV': '060200', 'DESC_PROV': 'CAJABAMBA', 'CDGO_PADRE': '060000'},
    {'CDGO_PROV': '060100', 'DESC_PROV': 'CAJAMARCA', 'CDGO_PADRE': '060000'},
    {'CDGO_PROV': '140200', 'DESC_PROV': 'CAJATAMBO', 'CDGO_PADRE': '140000'},
    {'CDGO_PROV': '070400', 'DESC_PROV': 'CALCA', 'CDGO_PADRE': '070000'},
    {'CDGO_PROV': '240100', 'DESC_PROV': 'CALLAO', 'CDGO_PADRE': '240000'},
    {'CDGO_PROV': '040300', 'DESC_PROV': 'CAMANA', 'CDGO_PADRE': '040000'},
    {'CDGO_PROV': '070500', 'DESC_PROV': 'CANAS', 'CDGO_PADRE': '070000'},
    {'CDGO_PROV': '070600', 'DESC_PROV': 'CANCHIS', 'CDGO_PADRE': '070000'},
    {'CDGO_PROV': '220400', 'DESC_PROV': 'CANDARAVE', 'CDGO_PADRE': '220000'},
    {'CDGO_PROV': '050200', 'DESC_PROV': 'CANGALLO', 'CDGO_PADRE': '050000'},
    {'CDGO_PROV': '140300', 'DESC_PROV': 'CANTA', 'CDGO_PADRE': '140000'},
    {'CDGO_PROV': '200300', 'DESC_PROV': 'CARABAYA', 'CDGO_PADRE': '200000'},
    {'CDGO_PROV': '040400', 'DESC_PROV': 'CARAVELI', 'CDGO_PADRE': '040000'},
    {'CDGO_PROV': '020400', 'DESC_PROV': 'CARHUAZ', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '021700', 'DESC_PROV': 'CARLOS FERMIN FITZCARRALD', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '020500', 'DESC_PROV': 'CASMA', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '040500', 'DESC_PROV': 'CASTILLA', 'CDGO_PADRE': '040000'},
    {'CDGO_PROV': '080400', 'DESC_PROV': 'CASTROVIRREYNA', 'CDGO_PADRE': '080000'},
    {'CDGO_PROV': '040200', 'DESC_PROV': 'CAYLLOMA', 'CDGO_PADRE': '040000'},
    {'CDGO_PROV': '140400', 'DESC_PROV': 'CAÑETE', 'CDGO_PADRE': '140000'},
    {'CDGO_PROV': '060300', 'DESC_PROV': 'CELENDIN', 'CDGO_PADRE': '060000'},
    {'CDGO_PROV': '010100', 'DESC_PROV': 'CHACHAPOYAS', 'CDGO_PADRE': '010000'},
    {'CDGO_PROV': '110800', 'DESC_PROV': 'CHANCHAMAYO', 'CDGO_PADRE': '110000'},
    {'CDGO_PROV': '120900', 'DESC_PROV': 'CHEPEN', 'CDGO_PADRE': '120000'},
    {'CDGO_PROV': '130100', 'DESC_PROV': 'CHICLAYO', 'CDGO_PADRE': '130000'},
    {'CDGO_PROV': '100200', 'DESC_PROV': 'CHINCHA', 'CDGO_PADRE': '100000'},
    {'CDGO_PROV': '030700', 'DESC_PROV': 'CHINCHEROS', 'CDGO_PADRE': '030000'},
    {'CDGO_PROV': '060600', 'DESC_PROV': 'CHOTA', 'CDGO_PADRE': '060000'},
    {'CDGO_PROV': '200400', 'DESC_PROV': 'CHUCUITO', 'CDGO_PADRE': '200000'},
    {'CDGO_PROV': '070700', 'DESC_PROV': 'CHUMBIVILCAS', 'CDGO_PADRE': '070000'},
    {'CDGO_PROV': '110900', 'DESC_PROV': 'CHUPACA', 'CDGO_PADRE': '110000'},
    {'CDGO_PROV': '080700', 'DESC_PROV': 'CHURCAMPA', 'CDGO_PADRE': '080000'},
    {'CDGO_PROV': '110200', 'DESC_PROV': 'CONCEPCION', 'CDGO_PADRE': '110000'},
    {'CDGO_PROV': '040600', 'DESC_PROV': 'CONDESUYOS', 'CDGO_PADRE': '040000'},
    {'CDGO_PROV': '010600', 'DESC_PROV': 'CONDORCANQUI', 'CDGO_PADRE': '010000'},
    {'CDGO_PROV': '230200', 'DESC_PROV': 'CONTRALMIRANTE VILLAR', 'CDGO_PADRE': '230000'},
    {'CDGO_PROV': '060400', 'DESC_PROV': 'CONTUMAZA', 'CDGO_PADRE': '060000'},
    {'CDGO_PROV': '250100', 'DESC_PROV': 'CORONEL PORTILLO', 'CDGO_PADRE': '250000'},
    {'CDGO_PROV': '020600', 'DESC_PROV': 'CORONGO', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '030500', 'DESC_PROV': 'COTABAMBAS', 'CDGO_PADRE': '030000'},
    {'CDGO_PROV': '070100', 'DESC_PROV': 'CUSCO', 'CDGO_PADRE': '070000'},
    {'CDGO_PROV': '060500', 'DESC_PROV': 'CUTERVO', 'CDGO_PADRE': '060000'},
    {'CDGO_PROV': '180200', 'DESC_PROV': 'DANIEL ALCIDES CARRION', 'CDGO_PADRE': '180000'},
    {'CDGO_PROV': '150700', 'DESC_PROV': 'DATEM DEL MARAÑON', 'CDGO_PADRE': '150000'},
    {'CDGO_PROV': '090300', 'DESC_PROV': 'DOS DE MAYO', 'CDGO_PADRE': '090000'},
    {'CDGO_PROV': '201200', 'DESC_PROV': 'EL COLLAO', 'CDGO_PADRE': '200000'},
    {'CDGO_PROV': '211000', 'DESC_PROV': 'EL DORADO', 'CDGO_PADRE': '210000'},
    {'CDGO_PROV': '070800', 'DESC_PROV': 'ESPINAR', 'CDGO_PADRE': '070000'},
    {'CDGO_PROV': '130200', 'DESC_PROV': 'FERREÑAFE', 'CDGO_PADRE': '130000'},
    {'CDGO_PROV': '170200', 'DESC_PROV': 'GENERAL SANCHEZ CERRO', 'CDGO_PADRE': '170000'},
    {'CDGO_PROV': '121100', 'DESC_PROV': 'GRAN CHIMU', 'CDGO_PADRE': '120000'},
    {'CDGO_PROV': '030600', 'DESC_PROV': 'GRAU', 'CDGO_PADRE': '030000'},
    {'CDGO_PROV': '090900', 'DESC_PROV': 'HUACAYBAMBA', 'CDGO_PADRE': '090000'},
    {'CDGO_PROV': '060700', 'DESC_PROV': 'HUALGAYOC', 'CDGO_PADRE': '060000'},
    {'CDGO_PROV': '210200', 'DESC_PROV': 'HUALLAGA', 'CDGO_PADRE': '210000'},
    {'CDGO_PROV': '090400', 'DESC_PROV': 'HUAMALIES', 'CDGO_PADRE': '090000'},
    {'CDGO_PROV': '050100', 'DESC_PROV': 'HUAMANGA', 'CDGO_PADRE': '050000'},
    {'CDGO_PROV': '050800', 'DESC_PROV': 'HUANCA SANCOS', 'CDGO_PADRE': '050000'},
    {'CDGO_PROV': '190300', 'DESC_PROV': 'HUANCABAMBA', 'CDGO_PADRE': '190000'},
    {'CDGO_PROV': '200500', 'DESC_PROV': 'HUANCANE', 'CDGO_PADRE': '200000'},
    {'CDGO_PROV': '080100', 'DESC_PROV': 'HUANCAVELICA', 'CDGO_PADRE': '080000'},
    {'CDGO_PROV': '110100', 'DESC_PROV': 'HUANCAYO', 'CDGO_PADRE': '110000'},
    {'CDGO_PROV': '050300', 'DESC_PROV': 'HUANTA', 'CDGO_PADRE': '050000'},
    {'CDGO_PROV': '090100', 'DESC_PROV': 'HUANUCO', 'CDGO_PADRE': '090000'},
    {'CDGO_PROV': '140800', 'DESC_PROV': 'HUARAL', 'CDGO_PADRE': '140000'},
    {'CDGO_PROV': '020100', 'DESC_PROV': 'HUARAZ', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '020800', 'DESC_PROV': 'HUARI', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '021900', 'DESC_PROV': 'HUARMEY', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '140600', 'DESC_PROV': 'HUAROCHIRI', 'CDGO_PADRE': '140000'},
    {'CDGO_PROV': '140500', 'DESC_PROV': 'HUAURA', 'CDGO_PADRE': '140000'},
    {'CDGO_PROV': '020700', 'DESC_PROV': 'HUAYLAS', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '080600', 'DESC_PROV': 'HUAYTARA', 'CDGO_PADRE': '080000'},
    {'CDGO_PROV': '100100', 'DESC_PROV': 'ICA', 'CDGO_PADRE': '100000'},
    {'CDGO_PROV': '170300', 'DESC_PROV': 'ILO', 'CDGO_PADRE': '170000'},
    {'CDGO_PROV': '040700', 'DESC_PROV': 'ISLAY', 'CDGO_PADRE': '040000'},
    {'CDGO_PROV': '060800', 'DESC_PROV': 'JAEN', 'CDGO_PADRE': '060000'},
    {'CDGO_PROV': '110300', 'DESC_PROV': 'JAUJA', 'CDGO_PADRE': '110000'},
    {'CDGO_PROV': '220300', 'DESC_PROV': 'JORGE BASADRE', 'CDGO_PADRE': '220000'},
    {'CDGO_PROV': '121000', 'DESC_PROV': 'JULCAN', 'CDGO_PADRE': '120000'},
    {'CDGO_PROV': '110400', 'DESC_PROV': 'JUNIN', 'CDGO_PADRE': '110000'},
    {'CDGO_PROV': '070900', 'DESC_PROV': 'LA CONVENCION', 'CDGO_PADRE': '070000'},
    {'CDGO_PROV': '050400', 'DESC_PROV': 'LA MAR', 'CDGO_PADRE': '050000'},
    {'CDGO_PROV': '040800', 'DESC_PROV': 'LA UNION', 'CDGO_PADRE': '040000'},
    {'CDGO_PROV': '210300', 'DESC_PROV': 'LAMAS', 'CDGO_PADRE': '210000'},
    {'CDGO_PROV': '130300', 'DESC_PROV': 'LAMBAYEQUE', 'CDGO_PADRE': '130000'},
    {'CDGO_PROV': '200600', 'DESC_PROV': 'LAMPA', 'CDGO_PADRE': '200000'},
    {'CDGO_PROV': '091000', 'DESC_PROV': 'LAURICOCHA', 'CDGO_PADRE': '090000'},
    {'CDGO_PROV': '090600', 'DESC_PROV': 'LEONCIO PRADO', 'CDGO_PADRE': '090000'},
    {'CDGO_PROV': '140100', 'DESC_PROV': 'LIMA', 'CDGO_PADRE': '140000'},
    {'CDGO_PROV': '150300', 'DESC_PROV': 'LORETO', 'CDGO_PADRE': '150000'},
    {'CDGO_PROV': '050500', 'DESC_PROV': 'LUCANAS', 'CDGO_PADRE': '050000'},
    {'CDGO_PROV': '010400', 'DESC_PROV': 'LUYA', 'CDGO_PADRE': '010000'},
    {'CDGO_PROV': '160200', 'DESC_PROV': 'MANU', 'CDGO_PADRE': '160000'},
    {'CDGO_PROV': '090500', 'DESC_PROV': 'MARAÑON', 'CDGO_PADRE': '090000'},
    {'CDGO_PROV': '210400', 'DESC_PROV': 'MARISCAL CACERES', 'CDGO_PADRE': '210000'},
    {'CDGO_PROV': '020900', 'DESC_PROV': 'MARISCAL LUZURIAGA', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '170100', 'DESC_PROV': 'MARISCAL NIETO', 'CDGO_PADRE': '170000'},
    {'CDGO_PROV': '150600', 'DESC_PROV': 'MARISCAL RAMON CASTILLA', 'CDGO_PADRE': '150000'},
    {'CDGO_PROV': '150100', 'DESC_PROV': 'MAYNAS', 'CDGO_PADRE': '150000'},
    {'CDGO_PROV': '200700', 'DESC_PROV': 'MELGAR', 'CDGO_PADRE': '200000'},
    {'CDGO_PROV': '201300', 'DESC_PROV': 'MOHO', 'CDGO_PADRE': '200000'},
    {'CDGO_PROV': '190400', 'DESC_PROV': 'MORROPON', 'CDGO_PADRE': '190000'},
    {'CDGO_PROV': '210100', 'DESC_PROV': 'MOYOBAMBA', 'CDGO_PADRE': '210000'},
    {'CDGO_PROV': '100300', 'DESC_PROV': 'NASCA', 'CDGO_PADRE': '100000'},
    {'CDGO_PROV': '022000', 'DESC_PROV': 'OCROS', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '120400', 'DESC_PROV': 'OTUZCO', 'CDGO_PADRE': '120000'},
    {'CDGO_PROV': '180300', 'DESC_PROV': 'OXAPAMPA', 'CDGO_PADRE': '180000'},
    {'CDGO_PROV': '141000', 'DESC_PROV': 'OYON', 'CDGO_PADRE': '140000'},
    {'CDGO_PROV': '120500', 'DESC_PROV': 'PACASMAYO', 'CDGO_PADRE': '120000'},
    {'CDGO_PROV': '090700', 'DESC_PROV': 'PACHITEA', 'CDGO_PADRE': '090000'},
    {'CDGO_PROV': '250200', 'DESC_PROV': 'PADRE ABAD', 'CDGO_PADRE': '250000'},
    {'CDGO_PROV': '190500', 'DESC_PROV': 'PAITA', 'CDGO_PADRE': '190000'},
    {'CDGO_PROV': '021000', 'DESC_PROV': 'PALLASCA', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '100500', 'DESC_PROV': 'PALPA', 'CDGO_PADRE': '100000'},
    {'CDGO_PROV': '050600', 'DESC_PROV': 'PARINACOCHAS', 'CDGO_PADRE': '050000'},
    {'CDGO_PROV': '071000', 'DESC_PROV': 'PARURO', 'CDGO_PADRE': '070000'},
    {'CDGO_PROV': '180100', 'DESC_PROV': 'PASCO', 'CDGO_PADRE': '180000'},
    {'CDGO_PROV': '120600', 'DESC_PROV': 'PATAZ', 'CDGO_PADRE': '120000'},
    {'CDGO_PROV': '051000', 'DESC_PROV': 'PAUCAR DEL SARA SARA', 'CDGO_PADRE': '050000'},
    {'CDGO_PROV': '071100', 'DESC_PROV': 'PAUCARTAMBO', 'CDGO_PADRE': '070000'},
    {'CDGO_PROV': '210900', 'DESC_PROV': 'PICOTA', 'CDGO_PADRE': '210000'},
    {'CDGO_PROV': '100400', 'DESC_PROV': 'PISCO', 'CDGO_PADRE': '100000'},
    {'CDGO_PROV': '190100', 'DESC_PROV': 'PIURA', 'CDGO_PADRE': '190000'},
    {'CDGO_PROV': '021100', 'DESC_PROV': 'POMABAMBA', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '090800', 'DESC_PROV': 'PUERTO INCA', 'CDGO_PADRE': '090000'},
    {'CDGO_PROV': '200100', 'DESC_PROV': 'PUNO', 'CDGO_PADRE': '200000'},
    {'CDGO_PROV': '250400', 'DESC_PROV': 'PURUS', 'CDGO_PADRE': '250000'},
    {'CDGO_PROV': '150900', 'DESC_PROV': 'PUTUMAYO', 'CDGO_PADRE': '150000'},
    {'CDGO_PROV': '071200', 'DESC_PROV': 'QUISPICANCHI', 'CDGO_PADRE': '070000'},
    {'CDGO_PROV': '021200', 'DESC_PROV': 'RECUAY', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '150400', 'DESC_PROV': 'REQUENA', 'CDGO_PADRE': '150000'},
    {'CDGO_PROV': '210500', 'DESC_PROV': 'RIOJA', 'CDGO_PADRE': '210000'},
    {'CDGO_PROV': '010500', 'DESC_PROV': 'RODRIGUEZ DE MENDOZA', 'CDGO_PADRE': '010000'},
    {'CDGO_PROV': '201100', 'DESC_PROV': 'SAN ANTONIO DE PUTINA', 'CDGO_PADRE': '200000'},
    {'CDGO_PROV': '061100', 'DESC_PROV': 'SAN IGNACIO', 'CDGO_PADRE': '060000'},
    {'CDGO_PROV': '061200', 'DESC_PROV': 'SAN MARCOS', 'CDGO_PADRE': '060000'},
    {'CDGO_PROV': '210600', 'DESC_PROV': 'SAN MARTIN', 'CDGO_PADRE': '210000'},
    {'CDGO_PROV': '061000', 'DESC_PROV': 'SAN MIGUEL', 'CDGO_PADRE': '060000'},
    {'CDGO_PROV': '061300', 'DESC_PROV': 'SAN PABLO', 'CDGO_PADRE': '060000'},
    {'CDGO_PROV': '200900', 'DESC_PROV': 'SAN ROMAN', 'CDGO_PADRE': '200000'},
    {'CDGO_PROV': '120300', 'DESC_PROV': 'SANCHEZ CARRION', 'CDGO_PADRE': '120000'},
    {'CDGO_PROV': '200800', 'DESC_PROV': 'SANDIA', 'CDGO_PADRE': '200000'},
    {'CDGO_PROV': '021300', 'DESC_PROV': 'SANTA', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '060900', 'DESC_PROV': 'SANTA CRUZ', 'CDGO_PADRE': '060000'},
    {'CDGO_PROV': '120700', 'DESC_PROV': 'SANTIAGO DE CHUCO', 'CDGO_PADRE': '120000'},
    {'CDGO_PROV': '110700', 'DESC_PROV': 'SATIPO', 'CDGO_PADRE': '110000'},
    {'CDGO_PROV': '190800', 'DESC_PROV': 'SECHURA', 'CDGO_PADRE': '190000'},
    {'CDGO_PROV': '021400', 'DESC_PROV': 'SIHUAS', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '051100', 'DESC_PROV': 'SUCRE', 'CDGO_PADRE': '050000'},
    {'CDGO_PROV': '190600', 'DESC_PROV': 'SULLANA', 'CDGO_PADRE': '190000'},
    {'CDGO_PROV': '220100', 'DESC_PROV': 'TACNA', 'CDGO_PADRE': '220000'},
    {'CDGO_PROV': '160300', 'DESC_PROV': 'TAHUAMANU', 'CDGO_PADRE': '160000'},
    {'CDGO_PROV': '190700', 'DESC_PROV': 'TALARA', 'CDGO_PADRE': '190000'},
    {'CDGO_PROV': '160100', 'DESC_PROV': 'TAMBOPATA', 'CDGO_PADRE': '160000'},
    {'CDGO_PROV': '220200', 'DESC_PROV': 'TARATA', 'CDGO_PADRE': '220000'},
    {'CDGO_PROV': '110500', 'DESC_PROV': 'TARMA', 'CDGO_PADRE': '110000'},
    {'CDGO_PROV': '080500', 'DESC_PROV': 'TAYACAJA', 'CDGO_PADRE': '080000'},
    {'CDGO_PROV': '210800', 'DESC_PROV': 'TOCACHE', 'CDGO_PADRE': '210000'},
    {'CDGO_PROV': '120100', 'DESC_PROV': 'TRUJILLO', 'CDGO_PADRE': '120000'},
    {'CDGO_PROV': '230100', 'DESC_PROV': 'TUMBES', 'CDGO_PADRE': '230000'},
    {'CDGO_PROV': '150500', 'DESC_PROV': 'UCAYALI', 'CDGO_PADRE': '150000'},
    {'CDGO_PROV': '071300', 'DESC_PROV': 'URUBAMBA', 'CDGO_PADRE': '070000'},
    {'CDGO_PROV': '010700', 'DESC_PROV': 'UTCUBAMBA', 'CDGO_PADRE': '010000'},
    {'CDGO_PROV': '050700', 'DESC_PROV': 'VICTOR FAJARDO', 'CDGO_PADRE': '050000'},
    {'CDGO_PROV': '050900', 'DESC_PROV': 'VILCAS HUAMAN', 'CDGO_PADRE': '050000'},
    {'CDGO_PROV': '121200', 'DESC_PROV': 'VIRU', 'CDGO_PADRE': '120000'},
    {'CDGO_PROV': '091100', 'DESC_PROV': 'YAROWILCA', 'CDGO_PADRE': '090000'},
    {'CDGO_PROV': '110600', 'DESC_PROV': 'YAULI', 'CDGO_PADRE': '110000'},
    {'CDGO_PROV': '140700', 'DESC_PROV': 'YAUYOS', 'CDGO_PADRE': '140000'},
    {'CDGO_PROV': '021500', 'DESC_PROV': 'YUNGAY', 'CDGO_PADRE': '020000'},
    {'CDGO_PROV': '201000', 'DESC_PROV': 'YUNGUYO', 'CDGO_PADRE': '200000'},
    {'CDGO_PROV': '230300', 'DESC_PROV': 'ZARUMILLA', 'CDGO_PADRE': '230000'}]

current_folder = os.path.dirname(os.path.abspath(__file__))


def get_districts():
    with open(os.path.join(current_folder, 'districts')) as handle:
        districts = json.loads(handle.read())
        # {'CDGO_DIST': '030101', 'DESC_DIST': 'ABANCAY', 'CDGO_PADRE': '030100'}
        return districts


def get_session():
    s = requests.Session()
    s.headers.update(HEADERS)
    return s


def get_locales(session, district_code: str):
    """
    :return list of locales with format

    {
        'CCODI_LOCAL': '5374',
        'CCODI_UBIGEO': '140130',
        'TNOMB_LOCAL': 'IE 593 LUIS FELIPE DE LAS CASAS GRIEVE',
        'TDIRE_LOCAL': 'CALLE SANDRO BOTTICELLI SN'
    },
    """
    url = f'{BASE_URL}mesas/locales/{district_code}'
    res = do_get(session, url)
    if res:
        return res.json()['locales']


def get_mesas(session, local):
    """

    :param session:
    :param local:
        {
            'CCODI_LOCAL': '5374',
            'CCODI_UBIGEO': '140130',
            'TNOMB_LOCAL': 'IE 593 LUIS FELIPE DE LAS CASAS GRIEVE',
            'TDIRE_LOCAL': 'CALLE SANDRO BOTTICELLI SN'
        },
    :return: [
        '048137',
        '048138',
        '048139',
        '048140',
        '048141',
    ]
    """
    local_id = local['CCODI_LOCAL']
    ubigeo = local['CCODI_UBIGEO']
    url = f'{BASE_URL}mesas/actas/11/{ubigeo}/{local_id}'
    res = do_get(session, url)
    if res:
        return [mesa['NUMMESA'] for mesa in res.json()['mesasVotacion']]


def get_actas(session, mesa_number: str):
    url = f'{BASE_URL}mesas/detalle/{mesa_number}'
    res = do_get(session, url)
    if res:
        try:
            res_json = res.json()
            acta_presidente = parse_acta_presidente(res_json)
            acta_congreso = parse_acta_congreso(res_json)
            acta_parlamento = parse_acta_parlamento(res_json)
            save(acta_presidente, mesa_number, 'presi')
            save(acta_congreso, mesa_number, 'congre')
            save(acta_parlamento, mesa_number, 'parla')
        except Exception:
            file_name = os.path.join(current_folder, 'failed_to_fetch_mesas.jl')
            with open(file_name, 'a+') as handle:
                handle.write(f'{mesa_number}\n')


def save(acta, mesa_number, acta_name):
    acta['mesa'] = mesa_number
    file_name = os.path.join(current_folder, f'{acta_name}.jl')
    with open(file_name, 'a+') as handle:
        handle.write(json.dumps(acta) + '\n')


def do_get(session, url, retry=0):
    sleep(randint(1, 40) /10)
    try:
        res = session.get(url, headers=HEADERS, timeout=10)
    except Exception as err:
        if retry > MAX_RETRIES:
            print(f'failed to fetch {err}')
            raise Exception(err)

        retry += 1
        sleep_time = 1 * retry * retry
        sleep(sleep_time)
        print(f'sleeping {sleep_time} seconds...')
        return do_get(session, url, retry)

    if res.status_code == 404:
        return None

    return res


def parse_acta_parlamento(res_json):
    procesos = res_json.get('procesos')
    proceso_parla = procesos.get('generalPar')
    acta_parla = proceso_parla.get('parlamento')
    acta_parla['votos'] = []

    for voto in proceso_parla.get('votos'):
        if 'VOTOS' in voto.get('AUTORIDAD'):
            try:
                acta_parla[voto.get('AUTORIDAD')] = int(voto.get('congresal'))
            except ValueError:
                acta_parla[voto.get('AUTORIDAD')] = 0
        else:
            acta_parla['votos'].append(voto)
    return acta_parla


def parse_acta_congreso(res_json):
    procesos = res_json.get('procesos')
    proceso_congreso = procesos.get('generalCon')
    acta_congreso = proceso_congreso.get('congresal')
    acta_congreso['votos'] = []
    for voto in proceso_congreso.get('votos'):
        if 'VOTOS' in voto.get('AUTORIDAD'):
            try:
                acta_congreso[voto.get('AUTORIDAD')] = int(voto.get('congresal'))
            except ValueError:
                acta_congreso[voto.get('AUTORIDAD')] = 0
        else:
            acta_congreso['votos'].append(voto)
    return acta_congreso


def parse_acta_presidente(res_json):
    procesos = res_json.get('procesos')
    proceso_presidente = procesos.get('generalPre')
    acta_presidente = proceso_presidente.get('presidencial')
    if 'N_CANDIDATOS' in acta_presidente:
        del acta_presidente['N_CANDIDATOS']
    if 'OBSERVACION' in acta_presidente:
        del acta_presidente['OBSERVACION']
    if 'OBSERVACION_TXT' in acta_presidente:
        del acta_presidente['OBSERVACION_TXT']

    for voto in proceso_presidente.get('votos'):
        partido = voto.get('AUTORIDAD')
        if partido:
            try:
                acta_presidente[partido] = int(voto.get('congresal'))
            except ValueError:
                acta_presidente[partido] = 0
    return acta_presidente


def fetch_all():
    session = get_session()

    for district in districts:
        print(f'\tfetching district {district}')
        locales = get_locales(session, district.get('CDGO_DIST'))

        for local in locales:
            print(f'\tfetching local {local}')
            mesas = get_mesas(session, local)

            for mesa in mesas:
                print(f'\tfetching mesa {mesa}')
                get_actas(session, mesa)


if __name__ == "__main__":
    fetch_all()
