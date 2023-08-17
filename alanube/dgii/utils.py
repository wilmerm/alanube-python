

import datetime
from decimal import Decimal
import logging
import re
from typing import Dict, List, Tuple, Iterable

from .exceptions import ValidationError
from .config import (
    CREDIT_NOTE_INDICATOR_DAYS,
    CREDIT_NOTE_INDICATOR_EXPIRED,
    CREDIT_NOTE_INDICATOR_NOT_EXPIRED,
    FIT_TYPES,
    INCOME_TYPES,
    ITEM_GOOD_SERVICE_INDICATORS,
    ITEM_BILLING_INDICATORS,
    MODIFICATION_CODES,
    NCF_B,
    NCF_E,
    NCF_E_32,
    NCF_E_34,
    NCF_E_41,
    NCF_E_43,
    NCF_E_46,
    NCF_E_47,
    NCF_SERIES,
    NUMBER_DEFAULT_MAX_VALUE,
    PAYMENT_ACCOUNT_TYPES,
    PAYMENT_METHOD_BONUS,
    PAYMENT_METHODS,
    PROVINCES_AND_MUNICIPALITIES,
    UNIT_MEASURES,
)


def compare_amounts_with_margin(amount1: Decimal, amount2: Decimal, margin: Decimal = 1):
    dif = abs(amount1 - amount2)
    return dif <= margin


def format_phone_number(number: str):
    """Formatea un número de teléfono en el formato ###-###-####.

    Args:
        number (str): Número de teléfono a formatear.

    Returns:
        str: Número de teléfono formateado en el formato ###-###-####.

    Example:
        >>> phone_number = "8095554444"
        >>> formatted_phone_number = format_phone_number(phone_number)
        >>> print(formatted_phone_number)
        809-555-4444
    """
    # Eliminar caracteres especiales y no numéricos
    number_clean = re.sub(r'\D', '', number)
    # Aplicar el formato ###-###-####
    formatted_number = re.sub(r'(\d{3})(\d{3})(\d{4})', r'\1-\2-\3', number_clean)
    return formatted_number


def validate_phone_number(number: str):
    clean_number = format_phone_number(number)
    return clean_number


def get_credit_note_indicator(date: datetime.date):
    date_more_days = date + datetime.timedelta(days=CREDIT_NOTE_INDICATOR_DAYS)
    if date_more_days < datetime.date.today():
        return CREDIT_NOTE_INDICATOR_EXPIRED
    return CREDIT_NOTE_INDICATOR_NOT_EXPIRED


def validate_credit_note_indicator(indicator: int):
    if not indicator in (CREDIT_NOTE_INDICATOR_EXPIRED, CREDIT_NOTE_INDICATOR_NOT_EXPIRED):
        raise ValidationError('El indicador %s no es válido.' % indicator)
    return indicator


def strdate_to_date(str_date: str, _format='%Y-%m-%d'):
    return datetime.strptime(str_date, _format).date()


def validate_date(date: datetime.date | str):
    if isinstance(date, str):
        date = strdate_to_date(date)
    if isinstance(date, datetime.datetime):
        date = date.date()
    return date


def get_ncf_range(ncf_from: str, ncf_until: str):
    serie1, code1, sequence1 = split_ncf(ncf_from, validate=True)
    serie2, code2, sequence2 = split_ncf(ncf_until, validate=True)

    # Validamos haciendo uso de esta función:
    count_ncf_sequence(ncf_from, ncf_until)

    return [f'{serie1}{code1}{n}' for n in range(int(sequence1), int(sequence2) + 1)]


def count_ncf_sequence(ncf_from: str, ncf_until: str):
    """Cuenta la cantidad de NCFs que hay en un rango de NCFs (secuencia).

    >>> count_ncf_sequence('E310000000001', 'E310000000010')
    10
    >>> count_ncf_sequence('E310000000010', 'E310000000020')
    11
    """
    serie1, code1, sequence1 = split_ncf(ncf_from, validate=True)
    serie2, code2, sequence2 = split_ncf(ncf_until, validate=True)

    sequence1 = int(sequence1)
    sequence2 = int(sequence2)

    if (serie1 != serie2) or (code1 != code2):
        raise ValidationError('Los tipos de NCFs no son iguales.')
    if sequence1 > sequence2:
        raise ValidationError('El NCF inicial es mayor al NCF final.')
    return (sequence2 - sequence1) + 1


def is_ncfs_types_equal(ncf_from: str, ncf_until: str):
    serie1, code1, sequence1 = split_ncf(ncf_from, validate=True)
    serie2, code2, sequence2 = split_ncf(ncf_until, validate=True)

    if (serie1 != serie2) or (code1 != code2):
        return False
    return True


def split_ncf(ncf: str, validate=False):
    """Divide el `ncf` en sus 3 partes (serie, código, sequence).

    Args:
    ----------
    * `ncf` (str): Comprobante fiscal a dividir.
    * `validate` (bool): Si es True, se validará con `validate_ncf(ncf)`.

    Use:
    ----------
    >>> split_ncf('E310000224062')
    ('E', '31', '0000224062')

    """
    if validate is True:
        ncf = validate_ncf(ncf)
    serie = ncf[0]
    code = ncf[1:3]
    sequence = ncf[3:]
    return (serie, code, sequence)


def to_camel_case(name: str):
    words = name.split('_')
    capitalized_words = [word.capitalize() for word in words]
    camel_case_string = ''.join(capitalized_words)
    camel_case_string = camel_case_string[0].lower() + camel_case_string[1:]
    return camel_case_string


def validate_ncf(ncf: str, specific_serie: str = None):
    """Valida que el formato del `ncf` sea el correcto.

    Args:
    -------
    * `specific_serie` (str): (`NCF_B` o `NCF_E`), si se indica, se validará
        también que el `ncf` corresponda con dicha serie.
    """
    assert specific_serie in (None, NCF_B, NCF_E), f'El argumento {specific_serie=} no es válido.'
    serie, code, sequence = split_ncf(ncf, validate=False)

    if specific_serie and specific_serie != serie:
        raise ValidationError('La serie "%s" no es "%s".' % (serie, specific_serie))

    if not sequence.isdigit():
        raise ValidationError('La secuencia "%s" no es numérica.' % sequence)

    if serie == NCF_B:
        if not code in NCF_SERIES[NCF_B]['codes']:
            raise ValidationError('Tipo "%s" no válido para serie "%s".' % (code, serie))
        if len(ncf) != NCF_SERIES[NCF_B]['length']:
            raise ValidationError(
                'Los comprobantes de serie "%s" deben ser longitud %d.'
                % (serie, NCF_SERIES[NCF_B]['length'])
            )
    elif serie == NCF_E:
        if not code in NCF_SERIES[NCF_E]['codes']:
            raise ValidationError('Tipo "%s" no válido para serie "%s".' % (code, serie))
        if len(ncf) != NCF_SERIES[NCF_E]['length']:
            raise ValidationError(
                'Los comprobantes de serie "%s" deben ser longitud %d.'
                % (serie, NCF_SERIES[NCF_E]['length'])
            )
    else:
        raise ValidationError('La serie "%s" no es válida.' % serie)

    return ncf


def validate_value_in(value, _in: Iterable, _default = ...):
    if not value in _in:
        if _default != ...:
            return _default
        raise ValidationError('El valor %s no está dentro del listado.' % value)
    return value


def validate_email(email: str):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return email
    raise ValidationError(f'El email {email} no es válido.')


def validate_web_site(web_site):
    pattern = r'^(?:https?:\/\/)?(?:www\.)?([\w\.-]+)(?:\.\w+)+$'
    match = re.match(pattern, web_site)
    if match:
        return match.group(1)
    raise ValidationError(f'El web_site {web_site} no es válido.')


def validate_fit_type(fit_type: str):
    if not fit_type in FIT_TYPES:
        raise ValidationError('El tipo de ajuste %s no es válido' % fit_type)
    return fit_type


def validate_item_good_service_indicator(indicator: int):
    if not indicator in ITEM_GOOD_SERVICE_INDICATORS:
        raise ValidationError('El indicador %s del item no es válido' % indicator)
    return indicator


def validate_item_billing_indicator(indicator: int):
    """Valida que el `indicator` sea uno de estos valores:

        * `0`: No Facturable
        * `1`: ITBIS 1 ítem gravado a ITBIS tasa1 (18%).
        * `2`: ITBIS 2 ítem gravado a ITBIS tasa2 (16%).
        * `3`: ITBIS 3 ítem gravado a ITBIS tasa3 (0%).
        * `4`: Exento (E)
    """
    if not indicator in ITEM_BILLING_INDICATORS:
        raise ValidationError('El indicador %s del item no es válido' % indicator)
    return indicator


def validate_income_type(income_type: int, ncf: str = None):
    """Valida que el tipo de ingreso esté dentro de los permitidos.

    Args:
    --------
        * `income_type` (int, opcional): Si se indica, se comprobará si el tipo
            de ingreso es válido para el tipo de `ncf` indicado.
    """
    # No aplica para estos tipos:
    if ncf and split_ncf(ncf)[1] in (NCF_E_41, NCF_E_43, NCF_E_47):
        logging.warning(f'{income_type=} no aplica para {ncf=}.')
        return None

    if not income_type in INCOME_TYPES:
        raise ValidationError('Tipo de ingreso %s no es válido.' % income_type)

    return income_type


def validate_modification_code(code: int):
    """Valida el código utilizado para indicar si el e-CF del comprobante fiscal
    modificado es con la finalidad de:

    1) Anulación total
    2) Corrige texto del comprobante fiscal modificado
    3) Corrige montos del NCF modificado
    4) Reemplazo NCF emitido en contingencia
    5) Referenciar Factura de Consumo Electrónica.
    """
    if not code in MODIFICATION_CODES:
        raise ValidationError('El código de modificación %s no es válido.' % code)
    return code


def validate_number(
        value: int | float | Decimal | str,
        min_value: Decimal | None = 0,
        max_value: Decimal | None = NUMBER_DEFAULT_MAX_VALUE
    ):
    if isinstance(value, (int, Decimal)):
        pass
    elif isinstance(value, float):
        value = Decimal(str(value))
    elif isinstance(value, str) and value.isdigit():
        value = Decimal(value)
    else:
        raise ValidationError(f'El valor "{value}" no es un valor numérico.')

    if min_value != None and value < min_value:
        raise ValidationError(f'El valor {value} es menor al mínimo {min_value}.')
    if max_value != None and value > max_value:
        raise ValidationError(f'El valor {value} es mayor al máximo {max_value}.')

    return value


def validate_payment_type(payment_type: int):
    if not payment_type in INCOME_TYPES:
        raise ValidationError('Tipo de pago %s no es válido.' % payment_type)
    return payment_type


def validate_payment_method(payment_method: int):
    if not payment_method in INCOME_TYPES:
        raise ValidationError('Forma de pago %s no es válida.' % payment_method)
    return payment_method


def validate_payment_account_type(payment_account_type: str, ncf: str = None):
    if payment_account_type == None:
        return None # El tipo de cuenta es opcional.
    if ncf and payment_account_type and split_ncf(ncf)[1] in (NCF_E_34, NCF_E_43):
        raise ValidationError('El tipo de cuenta debe ser None para los tipos de NCF 34 y 43.')
    if not payment_account_type in PAYMENT_ACCOUNT_TYPES:
        raise ValidationError(
            'El tipo de cuenta de pago %s no es válido.' % payment_account_type
        )
    return payment_account_type


# def validate_payment_form(payment: Dict[str, int | float | Decimal], ncf: str = None):
#     if len(payment) != 2 or not payment.get('paymentMethod') or not payment.get('paymentAmount'):
#         raise ValidationError('Debe tener solo 2 items (`paymentMethod` y `paymentAmount`).')

#     payment_method = validate_payment_method(payment['paymentMethod'])
#     payment_amount = validate_number(payment['paymentAmount'])
#     payment['paymentMethod'] = payment_method
#     payment['paymentAmount'] = payment_amount

#     if ncf:
#         ncf_serie, ncf_code, ncf_sequence = split_ncf(ncf)
#         ncf_not_valid_for_payment_method = (NCF_E_34, NCF_E_43)

#         if ncf_code in ncf_not_valid_for_payment_method and payment:
#             raise ValidationError(
#                 'La forma de pago no aplica para los tipos de ncf %s y %s' %
#                 ncf_not_valid_for_payment_method
#             )

#         # Si la forma de pago corresponde al tipo 5 (Bonos o Certificados de regalo)
#         # el e-CF debe ser tipo 32 (Factura Consumo Electrónica).
#         if payment_method == PAYMENT_METHOD_BONUS and ncf_code != NCF_E_32:
#             raise ValidationError(
#                 'Si la forma de pago corresponde al tipo 5 (Bonos o Certificados '
#                 'de regalo) el e-CF debe ser tipo 32 (Factura Consumo Electrónica).'
#             )

#     return payment


# def validate_payment_forms(payments: List[Dict[str, float]], ):
#     payment_forms_table_errors = []
#     validated_payments = []

#     for payment in payments:
#         try:
#             validated_payments.append(validate_payment_form(payment))
#         except ValidationError as e:
#             payment_forms_table_errors.append(f'Pago 1: {e}')

#     if payment_forms_table_errors:
#         raise ValidationError('\n'.join(payment_forms_table_errors))

#     return validated_payments


def validate_percentage(value: Decimal):
    if value < 0 or value > 99:
        raise ValidationError('El pocentaje debe estar comprendido entre 0 y 99.')
    return value


def get_province_from_municipality(municipality_code: str):
    for province_code in PROVINCES_AND_MUNICIPALITIES:
        municipalities = PROVINCES_AND_MUNICIPALITIES[province_code]['municipalities']
        if municipality_code in municipalities:
            return province_code
    raise KeyError('No existe el municipio con el código "%s".' % municipality_code)


def validate_municipality(municipality_code: str, province_code: str = None):
    if not municipality_code:
        return None
    municipality_code = str(municipality_code)
    try:
        _province_code = get_province_from_municipality(municipality_code)
    except KeyError as e:
        raise ValidationError(e)
    else:
        if province_code is not None and str(province_code) != _province_code:
            raise ValidationError(
                    'El municipio %s no pertenece al a provincia %s.' %
                    (municipality_code, province_code)
                )
    return municipality_code


def validate_province(province_code: str):
    if not province_code:
        return None
    province_code = str(province_code)
    if not province_code in PROVINCES_AND_MUNICIPALITIES:
        raise ValidationError('El código de prinvinvcia "%s" no existe.' % province_code)
    return province_code


def validate_rnc(rnc: int | str):
    rnc = str(rnc)
    rnc = re.sub(r'\D', '', rnc)
    if len(rnc) != 9 and len(rnc) != 11:
        raise ValidationError('El RNC %s no tiene un formato válido.' % rnc)
    return int(rnc)


def validate_tax_type(tax_type: int):
    raise NotImplementedError()


def validate_tax_amount_indicator(indicator: int, ncf: str = None):
    if not indicator:
        return None
    indicator = int(indicator)
    if not indicator in (0, 1):
        raise ValidationError(
            'El indicador %d no es válido, debe ser %d (no incluye impuestos) '
            'y %d (incluye impuestos)' % (indicator, 0, 1)
        )
    if ncf and split_ncf(ncf)[1] in (NCF_E_43, NCF_E_46, NCF_E_47):
        raise ValidationError(
            'Los tipos de NCF 43, 46 y 47 no aplican para indicar si el monto '
            'tiene impuestos incluidos o no.'
        )
    return indicator


def validate_unit_measure(unit_measure: int):
    if not unit_measure in UNIT_MEASURES:
        raise ValidationError('Unidad de médida %s no permitida.' % unit_measure)
    return unit_measure