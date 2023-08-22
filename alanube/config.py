from typing import NewType


DollarSign = NewType('$', str)
PercentSign = NewType('%', str)


API_URL = 'https://api.alanube.co/dom/v1/'

DEVELOPER_API_URL = 'https://sandbox.alanube.co/dom/v1/'


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
