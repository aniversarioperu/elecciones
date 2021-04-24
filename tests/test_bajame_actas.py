from unittest import TestCase
import json

from bajame_actas_2021 import parse_acta_presidente, parse_acta_congreso


class TestBajameActa2021(TestCase):
    def test_parse_acta_presidente(self):
        self.maxDiff = None

        with open('acta.json') as handle:
            acta_json = json.loads(handle.read())
            result = parse_acta_presidente(acta_json)
            expected = {
                'CCENT_COMPU': 'C44068',
                'CCODI_UBIGEO': '140130',
                'CCOPIA_ACTA': '05S',
                'DEPARTAMENTO': 'LIMA',
                'PROVINCIA': 'LIMA',
                'DISTRITO': 'SANTIAGO DE SURCO',
                'TDIRE_LOCAL': 'CALLE SANDRO BOTTICELLI SN',
                'TNOMB_LOCAL': 'IE 593 LUIS FELIPE DE LAS CASAS GRIEVE',
                'NNUME_HABILM': 300,
                'TOT_CIUDADANOS_VOTARON': 262,
                'ACCION POPULAR': 14,
                'ALIANZA PARA EL PROGRESO': 2,
                'AVANZA PAIS - PARTIDO DE INTEGRACION SOCIAL': 63,
                'DEMOCRACIA DIRECTA': 0,
                'EL FRENTE AMPLIO POR JUSTICIA, VIDA Y LIBERTAD': 0,
                'FUERZA POPULAR': 20,
                'JUNTOS POR EL PERU': 38,
                'PARTIDO DEMOCRATICO SOMOS PERU': 2,
                'PARTIDO MORADO': 24,
                'PARTIDO NACIONALISTA PERUANO': 0,
                'PARTIDO POLITICO NACIONAL PERU LIBRE': 7,
                'PARTIDO POPULAR CRISTIANO - PPC': 16,
                'PERU PATRIA SEGURA': 0,
                'PODEMOS PERU': 8,
                'RENOVACION POPULAR': 44,
                'RENACIMIENTO UNIDO NACIONAL': 1,
                'UNION POR EL PERU': 1,
                'VICTORIA NACIONAL': 13,
                'TOTAL VOTOS EMITIDOS': 262,
                'TOTAL VOTOS VALIDOS': 253,
                'TOT_CIUDADANOS_VOTARON': 262,
                'VOTOS EN BLANCO': 4,
                'VOTOS IMPUGNADOS': 0,
                'VOTOS NULOS': 5,
            }
            self.assertEqual(expected, result)

    def test_parse_acta_congreso(self):
        self.maxDiff = None

        with open('acta.json') as handle:
            acta_json = json.loads(handle.read())
            result = parse_acta_congreso(acta_json)
            expected = {
                'CCODI_UBIGEO': '140130',
                'TNOMB_LOCAL': 'IE 593 LUIS FELIPE DE LAS CASAS GRIEVE',
                'TDIRE_LOCAL': 'CALLE SANDRO BOTTICELLI SN',
                'CCENT_COMPU': 'C44068',
                'DEPARTAMENTO': 'LIMA',
                'PROVINCIA': 'LIMA',
                'CCOPIA_ACTA': '27I',
                'DISTRITO': 'SANTIAGO DE SURCO',
                'NNUME_HABILM': 300,
                'OBSERVACION': 'CONTABILIZADAS NORMALES',
                'OBSERVACION_TXT': 'ACTA ELECTORAL NORMAL',
                'N_CANDIDATOS': 34,
                'TOT_CIUDADANOS_VOTARON': 262,
                'TOTAL VOTOS EMITIDOS': 262,
                'TOTAL VOTOS VALIDOS': 253,
                'VOTOS EN BLANCO': 10,
                'VOTOS IMPUGNADOS': 0,
                'VOTOS NULOS': 10,
            }
            for key, value in result.items():
                self.assertEqual(value, result[key])

            self.assertEqual(20, len(result['votos']))
            self.assertEqual(
                'FRENTE POPULAR AGRICOLA FIA DEL PERU - FREPAP',
                result['votos'][0]['AUTORIDAD']
            )
            self.assertEqual(
                '1',
                result['votos'][0]['TOTAL_VOTOS1']
            )
