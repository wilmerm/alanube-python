
from typing import NewType


DollarSign = NewType('$', str)
PercentSign = NewType('%', str)


API_URL = 'https://api.alanube.co/dom/v1/'

DEVELOPER_API_URL = 'https://sandbox.alanube.co/dom/v1/'


# Sólo para Notas de Crédito que no tienen derecho a rebajar ITBIS.
CREDIT_NOTE_INDICATOR_DAYS = 30
CREDIT_NOTE_INDICATOR_EXPIRED = 1
"""Valor si fecha de emisión del e-CF afectado es > `CREDIT_NOTE_INDICATOR_DAYS`."""
CREDIT_NOTE_INDICATOR_NOT_EXPIRED = 0
"""Valor si fecha de emisión del e-CF afectado es <= `CREDIT_NOTE_INDICATOR_DAYS`."""


# Status
REGISTERED = 'REGISTERED' # Se registró el documento
TO_SEND = 'TO_SEND' # Se registró y está listo para ser enviado
FAILED = 'FAILED' # Falló el envió del documento, normalmente pasará porque se está enviando un eNFC que ya se envió
WAITING_RESPONSE = 'WAITING_RESPONSE' # Fue enviado y se encuentra en espera de respuesta de la DGII
TO_NOTIFY = 'TO_NOTIFY' # Obtuvo respuesta de la DGII y se notificará mediante el webhook registrado
FINISHED = 'FINISHED' # Su proceso ha finalizado

STATUS_LIST = [
    REGISTERED,
    TO_SEND,
    FAILED,
    WAITING_RESPONSE,
    TO_NOTIFY,
    FINISHED,
]


# Legal Status
REJECTED = 'REJECTED' # El documento fue rechazado
ACCEPTED = 'ACCEPTED' # El documento fue aceptado
ACCEPTED_WITH_OBSERVATIONS = 'ACCEPTED_WITH_OBSERVATIONS' # El documento fue aceptado parcialmente
IN_PROCESS = 'IN_PROCESS' # El documento se encuentra en proceso

LEGAL_STATUS_LIST = [
    REJECTED,
    ACCEPTED,
    ACCEPTED_WITH_OBSERVATIONS,
    IN_PROCESS,
]


FIT_TYPE_DISCOUNT = 'D'
FIT_TYPE_SURCHARGE = 'R'

FIT_TYPES = [
    FIT_TYPE_DISCOUNT,
    FIT_TYPE_SURCHARGE,
]


# Identifica si el ítem corresponde a Bien o Servicio.
ITEM_GOOD_INDICATOR = 1
ITEM_SERVICE_INDICATOR = 2

ITEM_GOOD_SERVICE_INDICATORS = [
    ITEM_GOOD_INDICATOR,
    ITEM_SERVICE_INDICATOR,
]


# Indica si el ítem es exento, si es gravado, o No facturable. Indicará las distintas tasas:
ITEM_BILLING_INDICATOR_0 = 0
"""No Facturable"""
ITEM_BILLING_INDICATOR_1 = 1
"""ITBIS 1 ítem gravado a ITBIS tasa1 (18%)."""
ITEM_BILLING_INDICATOR_2 = 2
"""ITBIS 1 ítem gravado a ITBIS tasa1 (16%)."""
ITEM_BILLING_INDICATOR_3 = 3
"""ITBIS 1 ítem gravado a ITBIS tasa1 (0%)."""
ITEM_BILLING_INDICATOR_4 = 4
"""Excento (E)"""

ITEM_BILLING_INDICATORS = {
    ITEM_BILLING_INDICATOR_0: 0,
    ITEM_BILLING_INDICATOR_1: 18,
    ITEM_BILLING_INDICATOR_2: 16,
    ITEM_BILLING_INDICATOR_3: 0,
    ITEM_BILLING_INDICATOR_4: 0,
}


# Tipos de documentos (type)
# Tipos de documentos enviados en el webhook de documento finalizado.
fiscalInvoice = 'fiscalInvoice'	# Factura de crédito fiscal (31)
invoice	= 'invoice' # Factura de consumo (32)
debitNote = 'debitNote' # Notas débito (33)
creditNote = 'creditNote' # Notas crédito (34)
specialRegime = 'specialRegime' # Factura para regímenes especiales (44)
gubernamental = 'gubernamental' # Facturas Gubernamentales (45)
exportSupport = 'exportSupport' # Facturas de Exportación (46)
purchase = 'purchase' # Compras (41)
minorExpense = 'minorExpense' # Gastos menores (43)
paymentAbroadSupport = 'paymentAbroadSupport' # Comprobante para Pagos al Exterior (47)

INVOICE_CODE_TYPES = {
    31: fiscalInvoice,
    32: invoice,
    33: debitNote,
    34: creditNote,
    44: specialRegime,
    45: gubernamental,
    46: exportSupport,
    41: purchase,
    43: minorExpense,
    47: paymentAbroadSupport
}


INCOME_TYPE_01 = 1 # Ingresos por operaciones (no financieros)
INCOME_TYPE_02 = 2 # Ingresos financieros
INCOME_TYPE_03 = 3 # Ingresos extraordinarios
INCOME_TYPE_04 = 4 # Ingresos por arrendamientos
INCOME_TYPE_05 = 5 # Ingresos por venta de activo depreciable
INCOME_TYPE_06 = 6 # Otros ingresos

INCOME_TYPES = [
    INCOME_TYPE_01,
    INCOME_TYPE_02,
    INCOME_TYPE_03,
    INCOME_TYPE_04,
    INCOME_TYPE_05,
    INCOME_TYPE_06,
]


MODIFICATION_CODE_1 = 1
"""1) Anulación total"""
MODIFICATION_CODE_2 = 2
"""2) Corrige texto del comprobante fiscal modificado"""
MODIFICATION_CODE_3 = 3
"""3) Corrige montos del NCF modificado"""
MODIFICATION_CODE_4 = 4
"""4) Reemplazo NCF emitido en contingencia"""
MODIFICATION_CODE_5 = 5
"""5) Referenciar Factura de Consumo Electrónica."""

MODIFICATION_CODES = [
    MODIFICATION_CODE_1,
    MODIFICATION_CODE_2,
    MODIFICATION_CODE_3,
    MODIFICATION_CODE_4,
    MODIFICATION_CODE_5,
]
"""
Código utilizado para indicar si el e-CF del comprobante fiscal modificado es con la finalidad de:
1) Anulación total
2) Corrige texto del comprobante fiscal modificado
3) Corrige montos del NCF modificado
4) Reemplazo NCF emitido en contingencia
5) Referenciar Factura de Consumo Electrónica.
"""


NCF_B = 'B'
NCF_B_01 = '01'
NCF_B_02 = '02'
NCF_B_03 = '03'
NCF_B_04 = '04'
NCF_B_11 = '11'
NCF_B_12 = '12'
NCF_B_13 = '13'
NCF_B_14 = '14'
NCF_B_15 = '15'
NCF_B_16 = '16'
NCF_B_17 = '17'

NCF_E = 'E'
"""Serie de Comprobantes Fiscales Electrónicos (e-CF)"""
NCF_E_31 = '31'
"""Factura de Crédito Fiscal Electrónico (Tipo 31)"""
NCF_E_32 = '32'
"""Factura de Consumo Electrónica (Tipo 32)"""
NCF_E_33 = '33'
"""Nota de Débito Electrónica (Tipo 33)"""
NCF_E_34 = '34'
"""Nota de Crédito Electrónica (Tipo 34)"""
NCF_E_41 = '41'
"""Compras Electrónico (Tipo 41)"""
NCF_E_43 = '43'
"""Gastos Menores Electrónico (Tipo 43)"""
NCF_E_44 = '44'
"""Regímenes Especiales Electrónico (Tipo 44)"""
NCF_E_45 = '45'
"""Gubernamental Electrónico (Tipo 45)"""
NCF_E_46 = '46'
"""Exportación Electrónico (Tipo 46)"""
NCF_E_47 = '47'
"""Pagos Exterior Electrónico (Tipo 47)"""

NCF_SERIES = {
    NCF_B: {
        'length': 11,
        'codes': [
            NCF_B_01,
            NCF_B_02,
            NCF_B_03,
            NCF_B_04,
            NCF_B_11,
            NCF_B_12,
            NCF_B_13,
            NCF_B_14,
            NCF_B_15,
            NCF_B_16,
            NCF_B_17,
        ],
    },
    NCF_E: {
        'length': 13,
        'codes': [
            NCF_E_31,
            NCF_E_32,
            NCF_E_33,
            NCF_E_34,
            NCF_E_41,
            NCF_E_43,
            NCF_E_44,
            NCF_E_45,
            NCF_E_46,
            NCF_E_47,
        ]
    }
}


NUMBER_DEFAULT_MAX_DIGIT = 18
NUMBER_DEFAULT_DECIMAL_PLACES = 2
NUMBER_DEFAULT_MAX_VALUE = 9999999999999999.99


PAYMENT_TYPE_CASH = 1
PAYMENT_TYPE_CREDIT = 2
PAYMENT_TYPE_FREE = 3

PAYMENT_TYPES = [
    PAYMENT_TYPE_CASH,
    PAYMENT_TYPE_CREDIT,
    PAYMENT_TYPE_FREE,
]

PAYMENT_METHOD_CASH = 1
PAYMENT_METHOD_TRANSFER = 2
PAYMENT_METHOD_CREDIT_CARD = 3
PAYMENT_METHOD_CREDIT = 4
PAYMENT_METHOD_BONUS = 5
PAYMENT_METHOD_SWAP = 6
PAYMENT_METHOD_CREDIT_NOTE = 7
PAYMENT_METHOD_OTHERS = 8

PAYMENT_METHODS = [
    PAYMENT_METHOD_CASH,
    PAYMENT_METHOD_TRANSFER,
    PAYMENT_METHOD_CREDIT_CARD,
    PAYMENT_METHOD_CREDIT,
    PAYMENT_METHOD_BONUS,
    PAYMENT_METHOD_SWAP,
    PAYMENT_METHOD_CREDIT_NOTE,
    PAYMENT_METHOD_OTHERS,
]

PAYMENT_ACCOUNT_TYPE_CT = 'CT'
"""Cuenta Corriente"""
PAYMENT_ACCOUNT_TYPE_AH = 'AH'
"""Cuenta de Ahorros"""
PAYMENT_ACCOUNT_TYPE_OT = 'OT'
"""Otra"""

PAYMENT_ACCOUNT_TYPES = [
    PAYMENT_ACCOUNT_TYPE_CT,
    PAYMENT_ACCOUNT_TYPE_AH,
    PAYMENT_ACCOUNT_TYPE_OT,
]


# Currencies
CURRENCIES = dict(
    BRL = 'BRL',    # REAL BRASILENO
    CAD = 'CAD',	# DOLAR CANADIENSE
    CHF = 'CHF',    # FRANCO SUIZO
    CHY = 'CHY',	# YUAN CHINO
    XDR = 'XDR',	# DERECHO ESPECIAL DE GIRO83
    DKK = 'DKK',	# CORONA DANESA
    ERU = 'EUR',	# EURO
    GBP = 'GBP',	# LIBRA ESTERLINA
    JPY = 'JPY',	# YEN JAPONES
    NOK = 'NOK',	# CORONA NORUEGA
    SCP = 'SCP',	# LIBRA ESCOCESA
    SEK = 'SEK',	# CORONA SUECA
    USD = 'USD',	# DOLAR ESTADOUNIDENSE
    VEF = 'VEF',	# BOLIVAR FUERTE VENEZOLANO
)


UNIT_MEASURES = {
    1: {'Abrev.': 'BARR', 'Medida': 'Barril'},
    2: {'Abrev.': 'BOL', 'Medida': 'Bolsa'},
    3: {'Abrev.': 'BOT', 'Medida': 'Bote'},
    4: {'Abrev.': 'BULTO', 'Medida': 'Bultos'},
    5: {'Abrev.': 'BOTELLA', 'Medida': 'Botella'},
    6: {'Abrev.': 'CAJ', 'Medida': 'Caja'},
    7: {'Abrev.': 'CAJETILLA', 'Medida': 'Cajetilla'},
    8: {'Abrev.': 'CM', 'Medida': 'Centímetro'},
    9: {'Abrev.': 'CIL', 'Medida': 'Cilindro'},
    10: {'Abrev.': 'CONJ', 'Medida': 'Conjunto'},
    11: {'Abrev.': 'CONT', 'Medida': 'Contenedor'},
    12: {'Abrev.': 'DÍA', 'Medida': 'Día'},
    13: {'Abrev.': 'DOC', 'Medida': 'Docena'},
    14: {'Abrev.': 'FARD', 'Medida': 'Fardo'},
    15: {'Abrev.': 'GL', 'Medida': 'Galones'},
    16: {'Abrev.': 'GRAD', 'Medida': 'Grado'},
    17: {'Abrev.': 'GR', 'Medida': 'Gramo'},
    18: {'Abrev.': 'GRAN', 'Medida': 'Granel'},
    19: {'Abrev.': 'HOR', 'Medida': 'Hora'},
    20: {'Abrev.': 'HUAC', 'Medida': 'Huacal'},
    21: {'Abrev.': 'KG', 'Medida': 'Kilogramo'},
    22: {'Abrev.': 'kWh', 'Medida': 'Kilovatio Hora'},
    23: {'Abrev.': 'LB', 'Medida': 'Libra'},
    24: {'Abrev.': 'LITRO', 'Medida': 'Litro'},
    25: {'Abrev.': 'LOT', 'Medida': 'Lote'},
    26: {'Abrev.': 'M', 'Medida': 'Metro'},
    27: {'Abrev.': 'M2', 'Medida': 'Metro Cuadrado'},
    28: {'Abrev.': 'M3', 'Medida': 'Metro Cúbico'},
    29: {'Abrev.': 'MMBTU', 'Medida': 'Millones de Unidades Térmicas'},
    30: {'Abrev.': 'MIN', 'Medida': 'Minuto'},
    31: {'Abrev.': 'PAQ', 'Medida': 'Paquete'},
    32: {'Abrev.': 'PAR', 'Medida': 'Par'},
    33: {'Abrev.': 'PIE', 'Medida': 'Pie'},
    34: {'Abrev.': 'PZA', 'Medida': 'Pieza'},
    35: {'Abrev.': 'ROL', 'Medida': 'Rollo'},
    36: {'Abrev.': 'SOBR', 'Medida': 'Sobre'},
    37: {'Abrev.': 'SEG', 'Medida': 'Segundo'},
    38: {'Abrev.': 'TANQUE', 'Medida': 'Tanque'},
    39: {'Abrev.': 'TONE', 'Medida': 'Tonelada'},
    40: {'Abrev.': 'TUB', 'Medida': 'Tubo'},
    41: {'Abrev.': 'YD', 'Medida': 'Yarda'},
    42: {'Abrev.': 'YD2', 'Medida': 'Yarda Cuadrada'},
    43: {'Abrev.': 'UND', 'Medida': 'Unidad'},
    44: {'Abrev.': 'EA', 'Medida': 'Elemento'},
    45: {'Abrev.': 'MILLAR', 'Medida': 'Millar'},
    46: {'Abrev.': 'SAC', 'Medida': 'Saco'},
    47: {'Abrev.': 'LAT', 'Medida': 'Lata'},
    48: {'Abrev.': 'DIS', 'Medida': 'Display'},
    49: {'Abrev.': 'BID', 'Medida': 'Bidón'},
    50: {'Abrev.': 'RAC', 'Medida': 'Ración'},
    51: {'Abrev.': 'Q', 'Medida': 'Quintal'},
    52: {'Abrev.': 'GRT', 'Medida': 'Toneladas de registro bruto'},
    53: {'Abrev.': 'P2', 'Medida': 'Pie cuadrado'},
    54: {'Abrev.': 'PAX', 'Medida': 'Pasajero'},
    55: {'Abrev.': 'PULG', 'Medida': 'Pulgadas'},
    56: {'Abrev.': 'STAY', 'Medida': 'Parqueo barcos en muelle'}
}


PROVINCES_AND_MUNICIPALITIES = {
    '010000': {
        'name': 'DISTRITO NACIONAL',
        'municipalities': {
            '010100': 'MUNICIPIO SANTO DOMINGO DE GUZMÁN',
            '010101': 'SANTO DOMINGO DE GUZMÁN (D. M.).',
        }
    },
    '020000': {
        'name': 'PROVINCIA AZUA',
        'municipalities': {
            '020100': 'MUNICIPIO AZUA',
            '020101': 'AZUA (D. M.).',
            '020102': 'BARRO ARRIBA (D. M.).',
            '020103': 'LAS BARÍAS-LA ESTANCIA (D. M.).',
            '020104': 'LOS JOVILLOS (D. M.).',
            '020105': 'PUERTO VIEJO (D. M.).',
            '020106': 'BARRERAS (D. M.).',
            '020107': 'DOÑA EMMA BALAGUER VIUDA VALLEJO (D. M.).',
            '020108': 'CLAVELLINA (D. M.).',
            '020109': 'LAS LOMAS (D. M.).',
            '020200': 'MUNICIPIO LAS CHARCAS',
            '020201': 'LAS CHARCAS (D. M.).',
            '020202': 'PALMAR DE OCOA (D. M.).',
            '020300': 'MUNICIPIO LAS YAYAS DE VIAJAMA',
            '020301': 'LAS YAYAS DE VIAJAMA (D. M.).',
            '020302': 'VILLARPANDO (D. M.).',
            '020303': 'HATO NUEVO CORTÉS (D. M.).',
            '020400': 'MUNICIPIO PADRE LAS CASAS',
            '020401': 'PADRE LAS CASAS (D. M.).',
            '020402': 'LAS LAGUNAS (D. M.).',
            '020403': 'LA SIEMBRA (D. M.).',
            '020404': 'MONTE BONITO (D. M.).',
            '020405': 'LOS FRÍOS (D. M.).',
            '020500': 'MUNICIPIO PERALTA',
            '020501': 'PERALTA (D. M.).',
            '020600': 'MUNICIPIO SABANA YEGUA',
            '020601': 'SABANA YEGUA (D. M.).',
            '020602': 'PROYECTO 4 (D. M.).',
            '020603': 'GANADERO (D. M.).',
            '020604': 'PROYECTO 2-C (D. M.).',
            '020700': 'MUNICIPIO PUEBLO VIEJO',
            '020701': 'PUEBLO VIEJO (D. M.).',
            '020702': 'EL ROSARIO (D. M.).',
            '020800': 'MUNICIPIO TÁBARA ARRIBA',
            '020801': 'TÁBARA ARRIBA (D. M.).',
            '020802': 'TÁBARA ABAJO (D. M.).',
            '020803': 'AMIAMA GÓMEZ (D. M.).',
            '020804': 'LOS TOROS (D. M.).',
            '020900': 'MUNICIPIO GUAYABAL',
            '020901': 'GUAYABAL (D. M.).',
            '021000': 'MUNICIPIO ESTEBANÍA',
            '021001': 'ESTEBANÍA (D. M.).',
        },
    },
    '030000': {
        'name': 'PROVINCIA BAHORUCO',
        'municipalities': {
            '030001': 'MUNICIPIO NEIBA',
            '030101': 'NEIBA (D. M.)',
            '030102': 'EL PALMAR (D. M.)',
            '030200': 'MUNICIPIO GALVÁN',
            '030201': 'GALVÁN (D. M.)',
            '030202': 'EL SALADO (D. M.)',
            '030300': 'MUNICIPIO TAMAYO',
            '030301': 'TAMAYO (D. M.)',
            '030302': 'UVILLA (D. M.)',
            '030303': 'SANTANA (D. M.)',
            '030304': 'MONSERRATE (MONTSERRAT) (D. M.)',
            '030305': 'CABEZA DE TORO (D. M.)',
            '030306': 'MENA (D. M.)',
            '030307': 'SANTA BÁRBARA EL 6 (D. M.)',
            '030400': 'MUNICIPIO VILLA JARAGUA',
            '030401': 'VILLA JARAGUA (D. M.)',
            '030500': 'MUNICIPIO LOS RÍOS',
            '030501': 'LOS RÍOS (D. M.)',
            '030502': 'LAS CLAVELLINAS (D. M.)'
        }
    },
    '040000': {
        'name': 'PROVINCIA BARAHONA',
        'municipalities': {
            '040100': 'MUNICIPIO BARAHONA',
            '040101': 'BARAHONA (D. M.)',
            '040102': 'EL CACHÓN (D. M.)',
            '040103': 'LA GUÁZARA (D. M.)',
            '040104': 'VILLA CENTRAL (D. M.)',
            '040200': 'MUNICIPIO CABRAL',
            '040201': 'CABRAL (D. M.)',
            '040300': 'MUNICIPIO ENRIQUILLO',
            '040301': 'ENRIQUILLO (D. M.)',
            '040302': 'ARROYO DULCE (D. M.)',
            '040400': 'MUNICIPIO PARAÍSO',
            '040401': 'PARAÍSO (D. M.)',
            '040402': 'LOS PATOS (D. M.)',
            '040500': 'MUNICIPIO VICENTE NOBLE',
            '040501': 'VICENTE NOBLE (D. M.)',
            '040502': 'CANOA (D. M.)',
            '040503': 'QUITA CORAZA (D. M.)',
            '040504': 'FONDO NEGRO (D. M.)',
            '040600': 'MUNICIPIO EL PEÑÓN',
            '040601': 'EL PEÑÓN (D. M.)',
            '040700': 'MUNICIPIO LA CIÉNAGA',
            '040701': 'LA CIÉNAGA (D. M.)',
            '040702': 'BAHORUCO (D. M.)',
            '040800': 'MUNICIPIO FUNDACIÓN',
            '040801': 'FUNDACIÓN (D. M.)',
            '040802': 'PESCADERÍA (D. M.)',
            '040900': 'MUNICIPIO LAS SALINAS',
            '040901': 'LAS SALINAS (D. M.)',
            '041000': 'MUNICIPIO POLO',
            '041001': 'POLO (D. M.)',
            '041100': 'MUNICIPIO JAQUIMEYES',
            '041101': 'JAQUIMEYES (D. M.)',
            '041102': 'PALO ALTO (D. M.)'
        }
    },
    '050000': {
        'name': 'PROVINCIA DAJABÓN',
        'municipalities': {
            '050100': 'MUNICIPIO DAJABÓN',
            '050101': 'DAJABÓN (D. M.)',
            '050102': 'CAÑONGO (D. M.)',
            '050200': 'MUNICIPIO LOMA DE CABRERA',
            '050201': 'LOMA DE CABRERA (D. M.)',
            '050202': 'CAPOTILLO (D. M.)',
            '050203': 'SANTIAGO DE LA CRUZ (D. M.)',
            '050300': 'MUNICIPIO PARTIDO',
            '050301': 'PARTIDO (D. M.)',
            '050400': 'MUNICIPIO RESTAURACIÓN',
            '050401': 'RESTAURACIÓN (D. M.)',
            '050500': 'MUNICIPIO EL PINO',
            '050501': 'EL PINO (D. M.)',
            '050502': 'MANUEL BUENO (D. M.)'
        }
    },
    '060000': {
        'name': 'PROVINCIA DUARTE',
        'municipalities': {
            '060100': 'MUNICIPIO SAN FRANCISCO DE MACORÍS',
            '060101': 'SAN FRANCISCO DE MACORÍS (D. M.)',
            '060102': 'LA PEÑA (D. M.)',
            '060103': 'CENOVÍ (D. M.)',
            '060104': 'JAYA (D. M.)',
            '060105': 'PRESIDENTE DON ANTONIO GUZMÁN FERNÁNDEZ (D. M.)',
            '060200': 'MUNICIPIO ARENOSO',
            '060201': 'ARENOSO (D. M.)',
            '060202': 'LAS COLES (D. M.)',
            '060203': 'EL AGUACATE (D. M.)',
            '060300': 'MUNICIPIO CASTILLO',
            '060301': 'CASTILLO (D. M.)',
            '060400': 'MUNICIPIO PIMENTEL',
            '060401': 'PIMENTEL (D. M.)',
            '060500': 'MUNICIPIO VILLA RIVA',
            '060501': 'VILLA RIVA (D. M.)',
            '060502': 'AGUA SANTA DEL YUNA (D. M.)',
            '060503': 'CRISTO REY DE GUARAGUAO (D. M.)',
            '060504': 'LAS TARANAS (D. M.)',
            '060505': 'BARRAQUITO (D. M.)',
            '060600': 'MUNICIPIO LAS GUÁRANAS',
            '060601': 'LAS GUÁRANAS (D. M.)',
            '060700': 'MUNICIPIO EUGENIO MARÍA DE HOSTOS',
            '060701': 'EUGENIO MARÍA DE HOSTOS (D. M.)',
            '060702': 'SABANA GRANDE (D. M.)'
        }
    },
    '070000': {
        'name': 'PROVINCIA ELÍAS PIÑA',
        'municipalities': {
            '070100': 'MUNICIPIO COMENDADOR',
            '070101': 'COMENDADOR (D. M.)',
            '070102': 'SABANA LARGA (D. M.)',
            '070103': 'GUAYABO (D. M.)',
            '070200': 'MUNICIPIO BÁNICA',
            '070201': 'BÁNICA (D. M.)',
            '070202': 'SABANA CRUZ (D. M.)',
            '070203': 'SABANA HIGÜERO (D. M.)',
            '070300': 'MUNICIPIO EL LLANO',
            '070301': 'EL LLANO (D. M.)',
            '070302': 'GUANITO (D. M.)',
            '070400': 'MUNICIPIO HONDO VALLE',
            '070401': 'HONDO VALLE (D. M.)',
            '070402': 'RANCHO DE LA GUARDIA (D. M.)',
            '070500': 'MUNICIPIO PEDRO SANTANA',
            '070501': 'PEDRO SANTANA (D. M.)',
            '070502': 'RÍO LIMPIO (D. M.)',
            '070600': 'MUNICIPIO JUAN SANTIAGO',
            '070601': 'JUAN SANTIAGO (D. M.)'
        }
    },
    '080000': {
        'name': 'PROVINCIA EL SEIBO',
        'municipalities': {
            '080100': 'MUNICIPIO EL SEIBO',
            '080101': 'EL SEIBO (D. M.)',
            '080102': 'PEDRO SÁNCHEZ (D. M.)',
            '080103': 'SAN FRANCISCO-VICENTILLO (D. M.)',
            '080104': 'SANTA LUCÍA (D. M.)',
            '080200': 'MUNICIPIO MICHES',
            '080201': 'MICHES (D. M.)',
            '080202': 'EL CEDRO (D. M.)',
            '080203': 'LA GINA (D. M.)'
        }
    },
    '090000': {
        'name': 'PROVINCIA ESPAILLAT',
        'municipalities': {
            '090100': 'MUNICIPIO MOCA',
            '090101': 'MOCA (D. M.)',
            '090102': 'JOSÉ CONTRERAS (D. M.)',
            '090103': 'SAN VÍCTOR (D. M.)',
            '090104': 'JUAN LÓPEZ (D. M.)',
            '090105': 'LAS LAGUNAS (D. M.)',
            '090106': 'CANCA LA REYNA (D. M.)',
            '090107': 'EL HIGÜERITO (D. M.)',
            '090108': 'MONTE DE LA JAGUA (D. M.)',
            '090109': 'LA ORTEGA (D. M.)',
            '090200': 'MUNICIPIO CAYETANO GERMOSÉN',
            '090201': 'CAYETANO GERMOSÉN (D. M.)',
            '090300': 'MUNICIPIO GASPAR HERNÁNDEZ',
            '090301': 'GASPAR HERNÁNDEZ (D. M.)',
            '090302': 'JOBA ARRIBA (D. M.)',
            '090303': 'VERAGUA (D. M.)',
            '090304': 'VILLA MAGANTE (D. M.)',
            '090400': 'MUNICIPIO JAMAO AL NORTE',
            '090401': 'JAMAO AL NORTE (D. M.)'
        }
    },
    '100000': {
        'name': 'PROVINCIA INDEPENDENCIA',
        'municipalities': {
            '100100': 'MUNICIPIO JIMANÍ',
            '100101': 'JIMANÍ (D. M.)',
            '100102': 'EL LIMÓN (D. M.)',
            '100103': 'BOCA DE CACHÓN (D. M.)',
            '100200': 'MUNICIPIO DUVERGÉ',
            '100201': 'DUVERGÉ (D. M.)',
            '100202': 'VENGAN A VER (D. M.)',
            '100300': 'MUNICIPIO LA DESCUBIERTA',
            '100301': 'LA DESCUBIERTA (D. M.)',
            '100400': 'MUNICIPIO POSTRER RÍO',
            '100401': 'POSTRER RÍO (D. M.)',
            '100402': 'GUAYABAL (D. M.)',
            '100500': 'MUNICIPIO CRISTÓBAL',
            '100501': 'CRISTÓBAL (D. M.)',
            '100502': 'BATEY 8 (D. M.)',
            '100600': 'MUNICIPIO MELLA',
            '100601': 'MELLA (D. M.)',
            '100602': 'LA COLONIA (D. M.)'
        }
    },
    '110000': {
        'name': 'PROVINCIA LA ALTAGRACIA',
        'municipalities': {
            '110100': 'MUNICIPIO HIGÜEY',
            '110101': 'HIGÜEY (D. M.)',
            '110102': 'LAS LAGUNAS DE NISIBÓN (D. M.)',
            '110103': 'LA OTRA BANDA (D. M.)',
            '110104': 'VERÓN PUNTA CANA (D. M.) (Incluye Bávaro)',
            '110200': 'MUNICIPIO SAN RAFAEL DEL YUMA',
            '110201': 'SAN RAFAEL DEL YUMA (D. M.)',
            '110202': 'BOCA DE YUMA (D. M.)',
            '110203': 'BAYAHÍBE (D. M.)'
        }
    },
    '120000': {
        'name': 'PROVINCIA LA ROMANA',
        'municipalities': {
            '120100': "MUNICIPIO LA ROMANA",
            '120101': "LA ROMANA (D. M.)",
            '120102': "CALETA (D. M.)",
            '120200': "MUNICIPIO GUAYMATE",
            '120201': "GUAYMATE (D. M.)",
            '120300': "MUNICIPIO VILLA HERMOSA",
            '120301': "VILLA HERMOSA (D. M.)",
            '120302': "CUMAYASA (D. M.)"
        }
    },
    '130000': {
        'name': 'PROVINCIA LA VEGA',
        'municipalities': {
            "130100": "MUNICIPIO LA VEGA",
            "130101": "LA VEGA (D. M.)",
            "130102": "RÍO VERDE ARRIBA (D. M.)",
            "130103": "EL RANCHITO (D. M.)",
            "130104": "TAVERAS (D. M.)",
            "130105": "DON JUAN RODRÍGUEZ (D.M.)",
            "130200": "MUNICIPIO CONSTANZA",
            "130201": "CONSTANZA (D. M.)",
            "130202": "TIREO (D. M.)",
            "130203": "LA SABINA (D. M.)",
            "130300": "MUNICIPIO JARABACOA",
            "130301": "JARABACOA (D. M.)",
            "130302": "BUENA VISTA (D. M.)",
            "130303": "MANABAO (D. M.)",
            "130400": "MUNICIPIO JIMA ABAJO",
            "130401": "JIMA ABAJO (D. M.)",
            "130402": "RINCÓN (D. M.)"
        }
    },
    '140000': {
        'name': 'PROVINCIA MARÍA TRINIDAD SÁNCHEZ',
        'municipalities': {
            "140100": "MUNICIPIO NAGUA",
            "140101": "NAGUA (D. M.)",
            "140102": "SAN JOSÉ DE MATANZAS (D. M.)",
            "140103": "LAS GORDAS (D. M.)",
            "140104": "ARROYO AL MEDIO (D. M.)",
            "140200": "MUNICIPIO CABRERA",
            "140201": "CABRERA (D. M.)",
            "140202": "ARROYO SALADO (D. M.)",
            "140203": "LA ENTRADA (D. M.)",
            "140300": "MUNICIPIO EL FACTOR",
            "140301": "EL FACTOR (D. M.)",
            "140302": "EL POZO (D. M.)",
            "140400": "MUNICIPIO RÍO SAN JUAN",
            "140401": "RÍO SAN JUAN (D. M.)"
        }
    },
    '150000': {
        'name': 'PROVINCIA MONTE CRISTI',
        'municipalities': {
            "150100": "MUNICIPIO MONTE CRISTI",
            "150101": "MONTE CRISTI (D. M.)",
            "150200": "MUNICIPIO CASTAÑUELAS",
            "150201": "CASTAÑUELAS (D. M.)",
            "150202": "PALO VERDE (D. M.)",
            "150300": "MUNICIPIO GUAYUBÍN",
            "150301": "GUAYUBÍN (D. M.)",
            "150302": "VILLA ELISA (D. M.)",
            "150303": "HATILLO PALMA (D. M.)",
            "150304": "CANA CHAPETÓN (D. M.)",
            "150400": "MUNICIPIO LAS MATAS DE SANTA CRUZ",
            "150401": "LAS MATAS DE SANTA CRUZ (D. M.)",
            "150500": "MUNICIPIO PEPILLO SALCEDO",
            "150501": "PEPILLO SALCEDO (MANZANILLO)",
            "150502": "SANTA MARÍA (D. M.)",
            "150600": "MUNICIPIO VILLA VÁSQUEZ",
            "150601": "VILLA VÁSQUEZ"
        }
    },
    '160000': {
        'name': 'PROVINCIA PEDERNALES',
        'municipalities': {
            "160100": "MUNICIPIO PEDERNALES",
            "160101": "PEDERNALES",
            "160102": "JOSÉ FRANCISCO PEÑA GÓMEZ (D. M.)",
            "160200": "MUNICIPIO OVIEDO",
            "160201": "OVIEDO",
            "160202": "JUANCHO (D. M.)"
        }
    },
    '170000': {
        'name': 'PROVINCIA PERAVIA',
        'municipalities': {
            "170100": "MUNICIPIO BANÍ",
            "170101": "BANÍ (D. M.)",
            "170102": "MATANZAS (D. M.)",
            "170103": "VILLA FUNDACIÓN (D. M.)",
            "170104": "SABANA BUEY (D. M.)",
            "170105": "PAYA (D. M.)",
            "170106": "VILLA SOMBRERO (D. M.)",
            "170107": "EL CARRETÓN (D. M.)",
            "170108": "CATALINA (D. M.)",
            "170109": "EL LIMONAL (D. M.)",
            "170110": "LAS BARÍAS (D. M.)",
            "170200": "MUNICIPIO NIZAO",
            "170201": "NIZAO",
            "170202": "PIZARRETE (D. M.)",
            "170203": "SANTANA (D. M.)",
            "170300": "MATANZAS",
            "170301": "MATANZAS"
        }
    },
    '180000': {
        'name': 'PROVINCIA PUERTO PLATA',
        'municipalities': {
            "180100": "MUNICIPIO PUERTO PLATA",
            "180101": "PUERTO PLATA (D. M.)",
            "180102": "YÁSICA ARRIBA (D. M.)",
            "180103": "MAIMÓN (D. M.)",
            "180200": "MUNICIPIO ALTAMIRA",
            "180201": "ALTAMIRA",
            "180202": "RÍO GRANDE (D. M.)",
            "180300": "MUNICIPIO GUANANICO",
            "180301": "GUANANICO",
            "180400": "MUNICIPIO IMBERT",
            "180401": "IMBERT",
            "180500": "MUNICIPIO LOS HIDALGOS",
            "180501": "LOS HIDALGOS",
            "180502": "NAVAS (D. M.)",
            "180600": "MUNICIPIO LUPERÓN",
            "180601": "LUPERÓN",
            "180602": "LA ISABELA (D. M.)",
            "180603": "BELLOSO (D. M.)",
            "180604": "EL ESTRECHO DE LUPERÓN OMAR BROSS (D. M.)",
            "180700": "MUNICIPIO SOSÚA",
            "180701": "SOSÚA",
            "180702": "CABARETE (D. M.)",
            "180703": "SABANETA DE YÁSICA (D. M.)",
            "180800": "MUNICIPIO VILLA ISABELA",
            "180801": "VILLA ISABELA",
            "180802": "ESTERO HONDO (D. M.)",
            "180803": "LA JAIBA (D. M.)",
            "180804": "GUALETE (D. M.)",
            "180900": "MUNICIPIO VILLA MONTELLANO",
            "180901": "VILLA MONTELLANO"
        }
    },
    '190000': {
        'name': 'PROVINCIA HERMANAS MIRABAL',
        'municipalities': {
            "190100": "MUNICIPIO SALCEDO",
            "190101": "SALCEDO",
            "190102": "JAMAO AFUERA (D. M.)",
            "190200": "MUNICIPIO TENARES",
            "190201": "TENARES",
            "190202": "BLANCO (D. M.)",
            "190300": "MUNICIPIO VILLA TAPIA",
            "190301": "VILLA TAPIA"
        }
    },
    '200000': {
        'name': 'PROVINCIA SAMANÁ',
        'municipalities': {
            "200100": "MUNICIPIO SAMANÁ",
            "200101": "SAMANÁ",
            "200102": "EL LIMÓN (D. M.)",
            "200103": "ARROYO BARRIL (D. M.)",
            "200104": "LAS GALERAS (D. M.)",
            "200200": "MUNICIPIO SÁNCHEZ",
            "200201": "SÁNCHEZ (D. M.)",
            "200300": "MUNICIPIO LAS TERRENAS",
            "200301": "LAS TERRENAS"
        }
    },
    '210000': {
        'name': 'PROVINCIA SAN CRISTÓBAL',
        'municipalities': {
            "210100": "MUNICIPIO SAN CRISTÓBAL",
            "210101": "SAN CRISTÓBAL (D. M.)",
            "210102": "HATO DAMAS (D. M.)",
            "210103": "HATILLO (D. M.)",
            "210200": "MUNICIPIO SABANA GRANDE DE PALENQUE",
            "210201": "SABANA GRANDE DE PALENQUE (D. M.)",
            "210300": "MUNICIPIO BAJOS DE HAINA",
            "210301": "BAJOS DE HAINA",
            "210302": "EL CARRIL (D. M.)",
            "210303": "QUITA SUEÑO (D. M.)",
            "210400": "MUNICIPIO CAMBITA GARABITOS",
            "210401": "CAMBITA GARABITOS",
            "210402": "CAMBITA EL PUEBLECITO (D. M.)",
            "210500": "MUNICIPIO VILLA ALTAGRACIA",
            "210501": "VILLA ALTAGRACIA",
            "210502": "SAN JOSÉ DEL PUERTO (D. M.)",
            "210503": "MEDINA (D. M.)",
            "210504": "LA CUCHILLA (D. M.)",
            "210600": "MUNICIPIO YAGUATE",
            "210601": "YAGUATE (D. M.)",
            "210602": "DOÑA ANA (D. M.)",
            "210700": "MUNICIPIO SAN GREGORIO DE NIGUA",
            "210701": "SAN GREGORIO DE NIGUA",
            "210800": "MUNICIPIO LOS CACAOS",
            "210801": "LOS CACAOS (D. M.)"
        }
    },
    '220000': {
        'name': 'PROVINCIA SAN JUAN',
        'municipalities': {
            "220100": "MUNICIPIO SAN JUAN",
            "220101": "SAN JUAN",
            "220102": "PEDRO CORTO (D. M.)",
            "220103": "SABANETA (D. M.)",
            "220104": "SABANA ALTA (D. M.)",
            "220105": "EL ROSARIO (D. M.)",
            "220106": "HATO DEL PADRE (D. M.)",
            "220107": "GUANITO (D. M.)",
            "220108": "LA JAGUA (D. M.)",
            "220109": "LAS MAGUANAS-HATO NUEVO (D. M.)",
            "220110": "LAS CHARCAS DE MARÍA NOVA (D. M.)",
            "220111": "LAS ZANJAS (D. M.)",
            "220200": "MUNICIPIO BOHECHÍO",
            "220201": "BOHECHÍO",
            "220202": "ARROYO CANO (D. M.)",
            "220203": "YAQUE (D. M.)",
            "220300": "MUNICIPIO EL CERCADO",
            "220301": "EL CERCADO",
            "220302": "DERRUMBADERO (D. M.)",
            "220303": "BATISTA (D. M.)",
            "220400": "MUNICIPIO JUAN DE HERRERA",
            "220401": "JUAN DE HERRERA",
            "220402": "JÍNOVA (D. M.)",
            "220500": "MUNICIPIO LAS MATAS DE FARFÁN",
            "220501": "LAS MATAS DE FARFÁN",
            "220502": "MATAYAYA (D. M.)",
            "220503": "CARRERA DE YEGUAS (D. M.)",
            "220600": "MUNICIPIO VALLEJUELO",
            "220601": "VALLEJUELO",
            "220602": "JORJILLO (D. M.)"
        }
    },
    '230000': {
        'name': 'PROVINCIA SAN PEDRO DE MACORÍS',
        'municipalities': {
            '230100': 'MUNICIPIO SAN PEDRO DE MACORÍS',
            '230101': 'SAN PEDRO DE MACORÍS',
            '230200': 'MUNICIPIO LOS LLANOS',
            '230201': 'LOS LLANOS',
            '230202': 'EL PUERTO (D. M.)',
            '230203': 'GAUTIER (D. M.)',
            '230300': 'MUNICIPIO RAMÓN SANTANA',
            '230301': 'RAMÓN SANTANA',
            '230400': 'MUNICIPIO CONSUELO',
            '230401': 'CONSUELO',
            '230500': 'MUNICIPIO QUISQUEYA',
            '230501': 'QUISQUEYA',
            '230600': 'MUNICIPIO GUAYACANES',
            '230601': 'GUAYACANES'
        }
    },
    '240000': {
        'name': 'PROVINCIA SÁNCHEZ RAMÍREZ',
        'municipalities': {
            '240100': 'MUNICIPIO COTUÍ',
            '240101': 'COTUÍ',
            '240102': 'QUITA SUEÑO (D. M.)',
            '240103': 'CABALLERO (D. M.)',
            '240104': 'COMEDERO ARRIBA (D. M.)',
            '240105': 'PLATANAL (D. M.)',
            '240106': 'ZAMBRANA ABAJO',
            '240200': 'MUNICIPIO CEVICOS',
            '240201': 'CEVICOS',
            '240202': 'LA CUEVA (D. M.)',
            '240300': 'MUNICIPIO FANTINO',
            '240301': 'FANTINO',
            '240400': 'MUNICIPIO LA MATA',
            '240401': 'LA MATA',
            '240402': 'LA BIJA (D. M.)',
            '240403': 'ANGELINA (D. M.)',
            '240404': 'HERNANDO ALONZO (D. M.)'
        }
    },
    '250000': {
        'name': 'PROVINCIA SANTIAGO',
        'municipalities': {
            '250100': 'MUNICIPIO SANTIAGO',
            '250101': 'SANTIAGO',
            '250102': 'PEDRO GARCÍA (D. M.)',
            '250104': 'BAITOA (D. M.)',
            '250105': 'LA CANELA (D. M.)',
            '250106': 'SAN FRANCISCO DE JACAGUA (D. M.)',
            '250107': 'HATO DEL YAQUE (D. M.)',
            '250200': 'MUNICIPIO BISONÓ',
            '250201': 'VILLA BISONÓ (NAVARRETE) (D. M.)',
            '250300': 'MUNICIPIO JÁNICO',
            '250301': 'JÁNICO',
            '250302': 'JUNCALITO (D. M.)',
            '250303': 'EL CAIMITO (D. M.)',
            '250400': 'MUNICIPIO LICEY AL MEDIO',
            '250401': 'LICEY AL MEDIO',
            '250402': 'LAS PALOMAS (D. M.)',
            '250500': 'MUNICIPIO SAN JOSÉ DE LAS MATAS',
            '250501': 'SAN JOSÉ DE LAS MATAS',
            '250502': 'EL RUBIO (D. M.)',
            '250503': 'LA CUESTA (D. M.)',
            '250504': 'LAS PLACETAS (D. M.)',
            '250600': 'MUNICIPIO TAMBORIL',
            '250601': 'TAMBORIL',
            '250602': 'CANCA LA PIEDRA (D. M.)',
            '250700': 'MUNICIPIO VILLA GONZÁLEZ',
            '250701': 'VILLA GONZÁLEZ',
            '250702': 'PALMAR ARRIBA (D. M.)',
            '250703': 'EL LIMÓN (D. M.)',
            '250800': 'MUNICIPIO PUÑAL',
            '250801': 'PUÑAL',
            '250802': 'GUAYABAL (D. M.)',
            '250803': 'CANABACOA (D. M.)',
            '250900': 'MUNICIPIO SABANA IGLESIA',
            '250901': 'SABANA IGLESIA',
            '251000': 'BAITOA'
        }
    },
    '260000': {
        'name': 'PROVINCIA SANTIAGO RODRÍGUEZ',
        'municipalities': {
            '260100': 'MUNICIPIO SAN IGNACIO DE SABANETA',
            '260101': 'SAN IGNACIO DE SABANETA (D. M.)',
            '260200': 'MUNICIPIO VILLA LOS ALMÁCIGOS',
            '260201': 'VILLA LOS ALMÁCIGOS (D. M.)',
            '260300': 'MUNICIPIO MONCIÓN',
            '260301': 'MONCIÓN (D. M.)'
        }
    },
    '270000': {
        'name': 'PROVINCIA VALVERDE',
        'municipalities': {
            '270100': 'MUNICIPIO MAO',
            '270101': 'MAO (D. M.)',
            '270102': 'AMINA (D. M.)',
            '270103': 'JAIBÓN (PUEBLO NUEVO) (D. M.)',
            '270104': 'GUATAPANAL (D. M.)'
        }
    },
    '280000': {
        'name': 'PROVINCIA MONSEÑOR NOUEL',
        'municipalities': {
            '280100': 'MUNICIPIO BONAO',
            '280101': 'BONAO (D. M.)',
            '280102': 'SABANA DEL PUERTO (D. M.)',
            '280103': 'JUMA BEJUCAL (D. M.)',
            '280104': 'ARROYO TORO - MASIPEDRO (D. M.)'
        }
    },
    '290000': {
        'name': 'PROVINCIA MONTE PLATA',
        'municipalities': {
            '290100': 'MUNICIPIO MONTE PLATA',
            '290101': 'MONTE PLATA (D. M.)',
            '290102': 'DON JUAN (D. M.)',
            '290103': 'CHIRINO (D. M.)',
            '290104': 'BOYÁ (D. M.)'
        }
    },
    '300000': {
        'name': 'PROVINCIA HATO MAYOR',
        'municipalities': {
            '300100': 'MUNICIPIO HATO MAYOR',
            '300101': 'HATO MAYOR (D. M.)',
            '300102': 'YERBA BUENA (D. M.)',
            '300103': 'MATA PALACIO (D. M.)',
            '300104': 'GUAYABO DULCE (D. M.)'
        }
    },
    '310000': {
        'name': 'PROVINCIA SAN JOSÉ DE OCOA',
        'municipalities': {
            '310100': 'MUNICIPIO SAN JOSÉ DE OCOA',
            '310101': 'SAN JOSÉ DE OCOA (D. M.)',
            '310102': 'LA CIÉNAGA (D. M.)',
            '310103': 'NIZAO - LAS AUYAMAS (D. M.)',
            '310104': 'EL PINAR (D. M.)'
        }
    },
    '320000': {
        'name': 'PROVINCIA SANTO DOMINGO',
        'municipalities': {
            '320100': 'MUNICIPIO SANTO DOMINGO ESTE',
            '320101': 'SANTO DOMINGO ESTE (D. M.)',
            '320102': 'SAN LUIS (D. M.)',
            '320200': 'MUNICIPIO SANTO DOMINGO OESTE',
            '320201': 'SANTO DOMINGO OESTE (D. M.)',
            '320300': 'MUNICIPIO SANTO DOMINGO NORTE',
            '320301': 'SANTO DOMINGO NORTE (D. M.)',
            '320302': 'LA VICTORIA (D. M.)',
            '320400': 'MUNICIPIO BOCA CHICA',
            '320401': 'BOCA CHICA (D. M.)',
            '320402': 'LA CALETA (D. M.)',
            '320500': 'MUNICIPIO SAN ANTONIO DE GUERRA',
            '320501': 'SAN ANTONIO DE GUERRA (D. M.)',
            '320502': 'HATO VIEJO (D. M.)',
            '320600': 'MUNICIPIO LOS ALCARRIZOS',
            '320601': 'LOS ALCARRIZOS (D. M.)',
            '320602': 'PALMAREJO-VILLA LINDA (D. M.)',
            '320603': 'PANTOJA (D. M.)',
            '320700': 'MUNICIPIO PEDRO BRAND',
            '320701': 'PEDRO BRAND (D. M.)',
            '320702': 'LA GUÁYIGA (D. M.)',
            '320703': 'LA CUABA (D. M.)'
        }
    }
}