
import datetime
from decimal import Decimal
from typing import Any, Dict, List, Tuple, Type
import logging

from .exceptions import ValidationError
from .config import (
    CURRENCIES,
    FIT_TYPES,
    ITEM_BILLING_INDICATOR_1,
    ITEM_BILLING_INDICATOR_2,
    ITEM_BILLING_INDICATOR_3,
    ITEM_BILLING_INDICATOR_4,
    ITEM_BILLING_INDICATORS,
    NCF_E,
    NCF_E_31,
    NCF_E_32,
    NCF_E_34,
    NCF_E_41,
    NCF_E_43,
    NCF_E_44,
    NCF_E_45,
    NCF_E_47,
    NCF_SERIES,
    NUMBER_DEFAULT_MAX_VALUE,
    PAYMENT_ACCOUNT_TYPES,
    PAYMENT_METHODS,
    PAYMENT_TYPE_CREDIT,
    PAYMENT_TYPES,
    UNIT_MEASURES,
    DollarSign,
    PercentSign,
)
from .utils import (
    compare_amounts_with_margin,
    count_ncf_sequence,
    format_phone_number,
    get_province_from_municipality,
    is_ncfs_types_equal,
    split_ncf,
    to_camel_case,
    validate_credit_note_indicator,
    validate_date,
    validate_email,
    validate_fit_type,
    validate_income_type,
    validate_item_billing_indicator,
    validate_item_good_service_indicator,
    validate_modification_code,
    validate_municipality,
    validate_ncf,
    validate_number,
    validate_payment_account_type,
    validate_payment_type,
    validate_percentage,
    validate_phone_number,
    validate_province,
    validate_rnc,
    validate_tax_amount_indicator,
    validate_tax_type,
    validate_unit_measure,
    validate_value_in,
    validate_web_site,
)
from .fields import (
    Field,
    IntField,
    NCFField,
    RNCField,
    StrField,
    DecimalField,
    DateField,
    UnitMeasureField,
    EmailField,
    PhoneField,
    FormField,
    ListField,
    ListFormField,
    Attr,
    NOT_IMPLEMENTED,
)


class Form:

    is_form = True
    dgii_name = None

    def __init__(self, **kwargs):
        for name, attr in self.__class__.__dict__.items():
            if not isinstance(attr, Field):
                continue

            field: Field = attr

            try:
                value = kwargs[name]
            except KeyError:
                # El campo tiene un valor default.
                if field.default != NOT_IMPLEMENTED:
                    value = field.get_default(self)
                # El campo puede ser nulo.
                elif field.null:
                    value = None
                # No se indicó el campo en los parámetros (y es obligatorio).
                else:
                    raise AttributeError(
                        f'No se indicó un valor para el campo {name} en {self}.'
                    )

            if value == None and not field.null:
                raise AttributeError(f'El campo {name} no puede ser nulo.')

            if value != None:
                value = self.__apply_field_validation(field, name, value)

            field.parent = self
            setattr(self, name, value)

    def __str__(self):
        return self.__class__.__name__.replace('Form', '')

    def __apply_field_validation(self, field: Field, name: str, value: any):
        value = field.validate(
            form=self,
            name=name,
            value=value,
        )
        return value

    @property
    def data(self):
        return self.get_data()

    def get_data(self, allow_null: bool = False, allow_blank: bool = False):
        """
        Obtiene los datos del objeto y los devuelve en forma de diccionario.

        Args:
            * `allow_null` (bool, optional): Permitir valores nulos.
            * `allow_blank` (bool, optional): Permitir string vacios.
        """
        validated_data = self.validate(vars(self))
        data = {}
        for name in validated_data:
            field = getattr(self.__class__, name)
            value = getattr(self, name)

            # Ejecutar validator personalizado.
            if hasattr(self, f'validate_{name}'):
                value = getattr(self, f'validate_{name}')(value, validated_data)

            # Omitir valores nulos si no se permite
            if value is None and allow_null is False:
                continue

            # Omitir valores en blanco si no se permite
            if value == '' and allow_blank is False:
                continue

            value = self.__parse(field, name, value)

            # Convertir el nombre a CamelCase
            name_camel_case = to_camel_case(name)
            data[name_camel_case] = value
        return data

    def validate(self, data: dict):
        return data

    def __parse(self, field: Field, name: str, value: Any):
        # Obtener los datos del objeto Form recursivamente
        if isinstance(value, Form):
            value = value.get_data()

        # Convertir fechas y datetime a formato ISO
        elif isinstance(value, (datetime.date, datetime.datetime)):
            if isinstance(value, datetime.datetime):
                value = value.date()
            value = value.isoformat()

        # Convertir valores Decimal a float (y reducir los decimales)
        elif isinstance(value, (float, Decimal)):
            decimal_places = field.decimal_places if field.decimal_places else 2
            value = round(float(value), decimal_places) # FIXME: La cantidad de decimales puede variar, hay algunos que llevan 4.

        elif isinstance(value, (list, tuple)):
            value = [self.__parse(field, name, v) for v in value]

        return value


class PaymentForm(Form):
    payment_method = IntField(
        'FormaPago',
        min_value=1,
        max_value=8,
        choices=PAYMENT_METHODS,
    )
    payment_amount = DecimalField(
        'MontoPago',
    )


class IdDocForm(Form):
    """
    Identificación del documento

    Args:
    * `company_id` (str): Identificador de la empresa.
    * `id_doc` (IdDocForm): Documento de identificación.
    * `sender` (SenderForm): Formulario del remitente.
    * `buyer` (BuyerForm): Formulario del comprador.
    * `additional_information` (AdditionalInformationForm, opcional): Información adicional.
    * `transport` (TransportForm, opcional): Formulario de transporte.
    * `totals` (TotalsForm): Formulario de totales.
    * `other_currency` (OtherCurrencyForm, opcional): Formulario de otra moneda.
    * `item_details` (List[ItemDetailForm]): Detalles de los elementos.
    * `subtotals` (List[SubtotalForm], opcional): Subtotales.
    * `discounts_or_surcharges` (List[DiscountsOrSurchargeForm], opcional): Descuentos o recargos.
    * `pagination` (List[PaginationForm], opcional): Paginación.
    * `information_reference` (InformationReferenceForm, opcional): Información de referencia.
    * `config` (ConfigForm, opcional): Configuración.
    * `encf` (str):
    * `sequence_due_date` (datetime.date):
    * `deferred_delivery_indicator` (int):
    * `tax_amount_indicator` (int):
    * `income_type` (int):
    * `payment_type` (int):
    * `payment_deadline` (datetime.date):
    * `payment_term` (str):
    * `payment_forms_table` (List[PaymentForm]):
    * `payment_account_type` (str):
    * `payment_account_number` (str):
    * `bank_payment` (str):
    * `date_from` (datetime.date):
    * `date_until` (datetime.date):
    * `total_pages` (int):
    """
    encf: str = NCFField(
        'eNCF',
        null=False,
    )
    sequence_due_date: datetime.date = DateField(
        'FechaVencimientoSecuencia',
        null=False
    )
    deferred_delivery_indicator: int = IntField(
        'IndicadorEnvioDiferido',
        max_value=1
    )
    tax_amount_indicator: int = IntField(
        'IndicadorMontoGravado',
        max_value=1,
        validators=[
            (validate_tax_amount_indicator, [Attr('encf')]),
        ],
    )
    income_type: int = IntField(
        'TipoIngresos',
        null=False,
        min_value=1,
        max_value=6,
        validators=[
            (validate_income_type, [Attr('encf')]),
        ]
    )
    payment_type: int = IntField(
        'TipoPago',
        null=False,
        min_value=1,
        max_value=3,
        choices=PAYMENT_TYPES,
        validators=[
            validate_payment_type,
        ]
    )
    payment_deadline: datetime.date = DateField(
        'FechaLimitePago',
    )
    payment_term = StrField(
        'TerminoPago',
        max_length=15,
    )
    payment_forms_table: List[PaymentForm] = ListFormField(
        'TablaFormasPago',
        form_class=PaymentForm,
        max_length=7,
    )
    payment_account_type: str = StrField(
        'TipoCuentaPago',
        max_length=2,
        choices=PAYMENT_ACCOUNT_TYPES,
        validators=[
            (validate_payment_account_type, [Attr('encf')]),
        ]
    )
    payment_account_number: str = StrField(
        'NumeroCuentaPago',
        max_length=28,
    )
    bank_payment: str = StrField(
        'BancoPago',
        max_length=75,
    )
    date_from: datetime.date = DateField(
        'FechaDesde',
    )
    date_until: datetime.date = DateField(
        'FechaHasta',
    )
    total_pages: int = IntField(
        'TotalPaginas',
        min_value=1,
        max_value=999,
    )

    def validate(self, data: dict):
        data = super().validate(data)

        if self.payment_deadline and self.payment_type != PAYMENT_TYPE_CREDIT:
            raise ValidationError({
                'payment_deadline': f'La fecha límite de pago no está permitida cuando el tipo de pago no es {PAYMENT_TYPE_CREDIT}'
            })

        return data


class SenderForm(Form):
    """
    Emisor de la factura.
    """
    rnc = RNCField(
        'RNCEmisor',
        null=False,
    )
    company_name = StrField(
        'RazonSocialEmisor',
        null=False,
        max_length=150,
    )
    tradename = StrField(
        'NombreComercial',
        max_length=150,
    )
    branch_office = StrField(
        'Sucursal',
        max_length=20,
    )
    address = StrField(
        'DireccionEmisor',
        null=False,
        max_length=100,
    )
    municipality = StrField(
        'Municipio',
        validators=[
            (validate_municipality, [Attr('province')]),
        ],
    )
    province = StrField(
        'Provincia',
        validators=[
            validate_province,
        ],
    )
    phone_number = ListField(
        'TablaTelefonoEmisor',
        field_class=PhoneField,
        max_length=3,
    )
    mail = EmailField(
        'CorreoEmisor',
    )
    web_site = StrField(
        'WebSite',
        max_length=50,
        validators=[
            validate_web_site,
        ]
    )
    economic_activity = StrField(
        'ActividadEconomica',
        max_length=100,
    )
    seller_code = StrField(
        'CodigoVendedor',
        max_length=60,
    )
    internal_invoice_number = IntField(
        'NumeroFacturaInterna',
        max_value=99999999999999999999,
    )
    internal_order_number = IntField(
        'NumeroPedidoInterno',
        max_value=99999999999999999999,
    )
    sale_area = StrField(
        'ZonaVenta',
        max_length=20,
    )
    sale_route = StrField(
        'RutaVenta',
        max_length=20,
    )
    additional_information_issuer = StrField(
        'InformacionAdicionalEmisor',
        max_length=250,
    )
    stamp_date = DateField(
        'FechaEmision',
        null=False,
    )



class BuyerForm(Form):
    rnc = RNCField(
        'RNCComprador',
    )
    company_name = StrField(
        'RazonSocialComprador',
        null=False,
        max_length=150,
    )
    contact = StrField(
        'ContactoComprador',
        max_length=80,
    )
    mail = EmailField(
        'CorreoComprador',
    )
    address = StrField(
        'DireccionComprador',
        max_length=100,
    )
    municipality = StrField(
        'Municipio',
        validators=[
            (validate_municipality, [Attr('province')]),
        ],
    )
    province = StrField(
        'Provincia',
        validators=[
            validate_province,
        ],
    )
    deliver_date = DateField(
        'FechaEntrega',
    )
    contact_delivery = StrField(
        'ContactoEntrega',
        max_length=100,
    )
    delivery_address = StrField(
        'DireccionEntrega',
        max_length=100,
    )
    additional_phone = PhoneField(
        'TelefonoAdicional',
    )
    purchase_order_date = DateField(
        'FechaOrdenCompra',
    )
    purchase_order_number = StrField(
        'NumeroOrdenCompra',
        max_length=20,
    )
    internal_code = StrField(
        'CodigoInternoComprador',
        max_length=20,
    )
    responsible_for_payment = StrField(
        'ResponsablePago',
        max_length=20,
    )
    additional_information = StrField(
        'InformacionAdicionalComprador',
        max_length=150,
    )


class AdditionalInformationForm(Form):
    """
    Información adicional del documento.
    """
    shipping_date = DateField(
        'FechaEmbarque',
    )
    shipment_number = StrField(
        'NumeroEmbarque',
        max_length=25,
    )
    container_number = StrField(
        'NumeroContenedor',
        max_length=100,
    )
    reference_number = IntField(
        'NumeroReferencia',
    )
    gross_weight = DecimalField(
        'PesoBruto',
    )
    net_weight = DecimalField(
        'PesoNeto',
    )
    gross_weight_unit = UnitMeasureField(
        'UnidadPesoBruto',
    )
    unit_net_weight = UnitMeasureField(
        'UnidadPesoNeto',
    )
    bulk_quantity = DecimalField(
        'CantidadBulto',
    )
    bulk_unit = UnitMeasureField(
        'UnidadBulto',
    )
    bulk_volume = DecimalField(
        'VolumenBulto',
    )
    unit_volume = UnitMeasureField(
        'UnidadVolumen',
    )


class TransportForm(Form):
    """
    Transporte.
    """
    driver = StrField(
        'Conductor',
        max_length=20,
    )
    transport_document = IntField(
        'DocumentoTransporte',
    )
    file = StrField(
        'Ficha',
        max_length=20,
    )
    license_plate = StrField(
        'Placa',
        max_length=7,
    )
    transportation_route = StrField(
        'RutaTransporte',
        max_length=20,
    )
    transportation_zone = StrField(
        'ZonaTransporte',
        max_length=20,
    )
    albaran_number = IntField(
        'NumeroAlbaran',
        max_value=20,
    )


class TotalsAdditionalTaxForm(Form):
    tax_type = IntField(
        'TipoImpuesto',
        null=True,
    )
    additional_tax_rate = DecimalField(
        'TasaImpuestoAdicional',
        max_value=999.99,
    )
    selective_tax_amount_specific_consumption = DecimalField(
        'MontoImpuestoSelectivoConsumoEspecifico',
    )
    amount_selective_consumption_tax_advalorem = DecimalField(
        'MontoImpuestoSelectivoConsumoAdvalorem',
    )
    other_additional_taxes = DecimalField(
        'OtrosImpuestosAdicionales',
    )


class TotalsForm(Form):
    """
    Totales para `InvoiceForm` y `CreditNoteForm`. Campo DGII <Totales>.

    ## Attrs:
    - `total_taxed_amount`: DecimalField - Total de la suma de valores de monto
    gravado ITBIS a diferentes tasas.

    - `i1_amount_taxed`: DecimalField - Total de la suma de valores de Ítems
    gravados asignados a ITBIS tasa 1 (tasa 18%).

    - `i2_amount_taxed`: DecimalField - Total de la suma de valores de Ítems
    gravados asignados a ITBIS tasa 2 (tasa 16%).

    - `i3_amount_taxed`: DecimalField - Total de la suma de valores de Ítems
    gravados asignados a ITBIS tasa 3 (tasa 0%).

    - `exempt_amount`: DecimalField - Total de la suma de valores de ítems exentos.

    - `itbis_s1`: IntField - Tasa de ITBIS 1 (18%).

    - `itbis_s2`: IntField - Tasa de ITBIS 2 (16%).

    - `itbis_s3`: IntField - Tasa de ITBIS 3 (0%).

    - `itbis_total`: DecimalField - Total de la suma de valores de ITBIS a
    diferentes tasas.

    - `itbis1_total`: DecimalField - Valor numérico igual a Monto Gravado ITBIS
    Tasa1 por la Tasa ITBIS 1.

    - `itbis2_total`: DecimalField - Valor numérico igual a Monto Gravado ITBIS
    Tasa2 por la Tasa ITBIS 2.

    - `itbis3_total`: DecimalField - Valor numérico igual a Monto gravado ITBIS
    Tasa3 por la Tasa ITBIS 3.

    - `additional_tax_amount`: DecimalField - Sumatoria de los campos Monto
    Impuesto Selectivo al Consumo Específico, Monto Impuesto Selectivo Ad
    Valorem y Monto Otros Impuestos Adicionales.

    - `additional_taxes`: ListFormField - Lista de impuestos adicionales que se
    pueden incluir.

    - `total_amount`: DecimalField - Monto Gravado Total + Monto exento +Total
    ITBIS + Monto del Impuesto adicional.

    - `non_billable_amount`: DecimalField - Total de la suma de montos de bienes
    o servicios con Indicador de facturación=0.

    - `amount_period`: DecimalField - Total de la suma de Monto Total y Monto no
    Facturable.

    - `previous_balance`: DecimalField - Saldo Anterior.

    - `amount_advance_payment`: DecimalField - Pago parcial por adelantado de la
    factura que se emite.

    - `pay_value`: DecimalField - Valor cobrado.

    - `itbis_total_retained`: DecimalField - Total de ITBIS retenido.

    - `isr_total_retention`: DecimalField - Monto del Impuesto Sobre la Renta
    correspondiente a la retención realizada de la prestación o locación de
    servicios. Condicional a que en la línea de detalle exista retención.

    - `itbis_total_perception`: DecimalField - Monto del ITBIS que el
    contribuyente cobra a terceros como adelanto del impuesto que éste percibirá
    en sus operaciones. Condicional a que en la línea de detalle exista percepción.

    - `isr_total_perception`: DecimalField - Monto del Impuesto Sobre la Renta
    que el contribuyente cobra a terceros como adelanto del impuesto que éste
    percibirá en sus operaciones. Condicional a que en la línea de detalle
    exista percepción.
    """

    total_taxed_amount: Decimal = DecimalField(
        'MontoGravadoTotal',
        help_text='Total de la suma de valores de monto gravado ITBIS a '
        'diferentes tasas. Condicional a que exista Monto gravado1, y/o Monto '
        'gravado 2 y/o Monto gravado 3.'
    )
    i1_amount_taxed: Decimal = DecimalField(
        'MontoGravadoI1',
        help_text='Total de la suma de valores de Ítems gravados asignados a '
        'ITBIS tasa 1 (tasa 18%), menos descuentos más recargos. 12 Condicional '
        'a que en la línea de detalle exista algún ítem gravado a tasa ITBIS1.'
    )
    i2_amount_taxed: Decimal = DecimalField(
        'MontoGravadoI2',
        help_text='Total de la suma de valores de Ítems gravados asignados a '
        'ITBIS tasa 2(tasa 16%), menos descuentos más recargos. Condicional a '
        'que en la línea de detalle exista algún ítem gravado a tasa ITBIS2.'
    )
    i3_amount_taxed: Decimal = DecimalField(
        'MontoGravadoI3',
        help_text='Total de la suma de valores de Ítems gravados asignados a '
        'ITBIS tasa 3 (tasa 0%), menos descuentos más recargos. Condicional a '
        'que en la línea de detalle exista algún ítem gravado a tasa ITBIS3.'
    )
    exempt_amount: Decimal = DecimalField(
        'MontoExento',
        help_text='Total de la suma de valores de ítems exentos, menos '
        'descuentos más recargos. Condicional a que en la línea de detalle '
        'exista algún ítem exento.'
    )
    itbis_s1: int = IntField(
        'ITBIS1',
        max_value=99,
        default=ITEM_BILLING_INDICATORS[ITEM_BILLING_INDICATOR_1],
        help_text='Tasa de ITBIS 1 (18%). Condicional a que en la línea de '
        'detalle exista ítem gravado a tasa 1.'
    )
    itbis_s2: int = IntField(
        'ITBIS2',
        max_value=99,
        default=ITEM_BILLING_INDICATORS[ITEM_BILLING_INDICATOR_2],
        help_text='Tasa de ITBIS 2 (16%). Condicional a que en la línea de '
        'detalle exista ítem gravado a tasa 2.'
    )
    itbis_s3: int = IntField(
        'ITBIS3',
        max_value=99,
        default=ITEM_BILLING_INDICATORS[ITEM_BILLING_INDICATOR_3],
        help_text='Tasa de ITBIS 3 (0%). Condicional a que en la línea de '
        'detalle exista ítem gravado a tasa 3.'
    )
    itbis_total: Decimal = DecimalField(
        'TotalITBIS',
        help_text='Total de la suma de valores de ITBIS a diferentes tasas. '
        'Condicional a que exista Total ITBIS Tasa 1, y/o Total ITBIS Tasa 2 '
        'y/o Total ITBIS Tasa 3.'
    )
    itbis1_total: Decimal = DecimalField(
        'TotalITBIS1',
        help_text='Valor numérico igual a Monto Gravado ITBIS Tasa1 por la '
        'Tasa ITBIS 1. Condicional a que exista Monto Gravado tasa 1 y tasa '
        'ITBIS 1. Si existen impuestos selectivos al consumo que formen parte '
        'de la base imponible del ITBIS, estos se sumaran al monto gravado '
        'antes de multiplicarlo por la tasa de ITBIS.'
    )
    itbis2_total: Decimal = DecimalField(
        'TotalITBIS2',
        help_text='Valor numérico igual a Monto Gravado ITBIS Tasa2*tasa ITBIS 2. '
        'Condicional a que exista Monto Gravado tasa 2 y tasa ITBIS 2.'
    )
    itbis3_total: Decimal = DecimalField(
        'TotalITBIS3',
        help_text='Valor numérico igual a Monto gravado ITBIS Tasa3*tasa ITBIS 3. '
        'Condicional a que exista Monto Gravado tasa 3 y tasa ITBIS 3.'
    )
    additional_tax_amount: Decimal = DecimalField(
        'MontoImpuestoAdicional',
        help_text='Sumatoria de los campos Monto Impuesto Selectivo al Consumo '
        'Específico, Monto Impuesto Selectivo Ad Valorem y Monto Otros '
        'Impuestos Adicionales.'
    )
    additional_taxes: List[TotalsAdditionalTaxForm] = ListFormField(
        'ImpuestosAdicionales',
        form_class=TotalsAdditionalTaxForm,
        max_length=20,
        help_text='Se pueden incluir 20 repeticiones de pares código - valor.'
    )
    total_amount: Decimal = DecimalField(
        'MontoTotal',
        help_text='Monto Gravado Total + Monto exento +Total ITBIS + Monto del '
        'Impuesto adicional.'
    )
    non_billable_amount: Decimal = DecimalField(
        'MontoNoFacturable',
        help_text='Total de la suma de montos de bienes o servicios con '
        'Indicador de facturación=0. Condicional a que en la línea de detalle '
        'exista algún ítem con indicador facturación igual a cero (0).'
    )
    amount_period: Decimal = DecimalField(
        'MontoPeriodo',
        help_text='Total de la suma de Monto Total y Monto no Facturable.'
    )
    previous_balance: Decimal = DecimalField(
        'SaldoAnterior',
        help_text='Saldo Anterior. Se incluye sólo con fines de ilustrar con '
        'claridad el cobro.'
    )
    amount_advance_payment: Decimal = DecimalField(
        'MontoAvancePago',
        help_text='Pago parcial por adelantado de la factura que se emite.'
    )
    pay_value: Decimal = DecimalField(
        'ValorPagar',
        help_text='Valor cobrado.'
    )

    # Campos únicamente para `CreditNoteForm`.

    itbis_total_retained: Decimal = DecimalField(
        'TotalITBISRetenido',
        help_text='Monto del ITBIS correspondiente a la retención que será '
        'realizada por el comprador. Condicional a que en la línea de detalle '
        'exista retención.'
    )
    isr_total_retention: Decimal = DecimalField(
        'TotalISRRetencion',
        help_text='Monto del Impuesto Sobre la Renta correspondiente a la '
        'retención realizada de la prestación o locación de servicios. '
        'Condicional a que en la línea de detalle exista retención.'
    )
    itbis_total_perception: Decimal = DecimalField(
        'TotalITBISPercepcion',
        help_text='Monto del ITBIS que el contribuyente cobra a terceros como '
        'adelanto del impuesto que éste percibirá en sus operaciones. '
        'Condicional a que en la línea de detalle exista percepción.'
    )
    isr_total_perception: Decimal = DecimalField(
        'TotalISRPercepcion',
        help_text='Monto del Impuesto Sobre la Renta que el contribuyente '
        'cobra a terceros como adelanto del impuesto que éste percibirá en sus '
        'operaciones. Condicional a que en la línea de detalle exista percepción.'
    )

    def validate_total_amount(self, total_amount: Decimal, data: dict):
        total_amount = Decimal(total_amount)
        total_taxed_amount = self.total_taxed_amount or 0
        exempt_amount = self.exempt_amount or 0
        itbis_total = self.itbis_total or 0
        additional_tax_amount = self.additional_tax_amount or 0
        total_amount_sum = sum((total_taxed_amount, exempt_amount, itbis_total, additional_tax_amount))

        if not compare_amounts_with_margin(total_amount, total_amount_sum):
            raise ValidationError(
                f'El valor de {total_amount=} no es igual a la sumatoria de '
                f'{total_taxed_amount=}, {exempt_amount=}, {itbis_total=} y {additional_tax_amount=}.'
            )

        return total_amount

    def validate_total_taxed_amount(self, total_taxed_amount: Decimal | None, data: dict):
        if total_taxed_amount == None:
            return None
        i1_amount_taxed = self.i1_amount_taxed or 0
        i2_amount_taxed = self.i2_amount_taxed or 0
        i3_amount_taxed = self.i3_amount_taxed or 0
        itbis123_totals = sum((i1_amount_taxed, i2_amount_taxed, i3_amount_taxed))

        if total_taxed_amount != None and total_taxed_amount != itbis123_totals:
            raise ValidationError(
                f'La sumatoria de los valores {i1_amount_taxed=} + {i2_amount_taxed=} + {i3_amount_taxed=} '
                f'no coinciden con el valor de {total_taxed_amount=}.'
            )
        return total_taxed_amount

    def validate_itbis_total(self, itbis_total: Decimal | None, data: dict):
        if not itbis_total:
            return None
        itbis_total = Decimal(itbis_total)

        # Total de la suma de valores de ITBIS a diferentes tasas. Condicional a
        # que exista Total ITBIS Tasa 1, y/o Total ITBIS Tasa 2 y/o Total ITBIS Tasa 3.
        itbis1_total = self.itbis1_total or 0
        itbis2_total = self.itbis2_total or 0
        itbis3_total = self.itbis3_total or 0

        if itbis_total != sum((itbis1_total, itbis2_total, itbis3_total)):
            raise ValidationError(
                f'El valor de {itbis_total=} no es igual a la sumatoria de '
                f'{itbis1_total=}, {itbis2_total=} y {itbis3_total=}.'
            )
        return itbis_total


class AdditionalTaxOtherCurrencyForm(Form):
    tax_type_other_currency = IntField(
        'TipoImpuestoOtraMoneda',
        null=False,
    )
    additional_tax_rate_other_currency = DecimalField(
        'TasaImpuestoAdicionalOtraMoneda',
        max_value=999.99,
    )
    selective_tax_amount_specific_consumption_other_currency = DecimalField(
        'MontoImpuestoSelectivoConsumoEspecificoOtraMoneda',
    )
    amount_selective_consumption_tax_advalorem_other_currency = DecimalField(
        'MontoImpuestoSelectivoConsumoAdvaloremOtraMoneda',
    )
    other_additional_taxes_other_currency = DecimalField(
        'OtrosImpuestosAdicionalesOtraMoneda',
    )


class OtherCurrencyForm(Form):
    currency_type = StrField(
        'TipoMoneda',
        null=False,
        max_length=3,
        choices=CURRENCIES,
    )
    exchange_rate = DecimalField(
        'TipoCambio',
        null=False,
        max_value=999.9999,
    )
    total_taxed_amount_other_currency = DecimalField(
        'MontoGravadoTotalOtraMoneda',
    )
    amount_taxed1_other_currency = DecimalField(
        'MontoGravado1OtraMoneda',
    )
    amount_taxed2_other_currency = DecimalField(
        'MontoGravado2OtraMoneda',
    )
    amount_taxed3_other_currency = DecimalField(
        'MontoGravado3OtraMoneda',
    )
    exempt_amount_other_currency = DecimalField(
        'MontoExentoOtraMoneda',
    )
    itbis_total_other_currency = DecimalField(
        'TotalITBISOtraMoneda',
    )
    itbis1_total_other_currency = DecimalField(
        'TotalITBIS1OtraMoneda',
    )
    itbis2_total_other_currency = DecimalField(
        'TotalITBIS2OtraMoneda',
    )
    itbis3_total_other_currency = DecimalField(
        'TotalITBIS3OtraMoneda',
    )
    additional_tax_amount_other_currency = DecimalField(
        'MontoImpuestoAdicionalOtraMoneda',
    )
    additional_taxes_other_currency = ListFormField(
        'ImpuestosAdicionalesOtraMoneda',
        form_class=AdditionalTaxOtherCurrencyForm,
        max_length=20,
    )
    total_amount_other_currency = DecimalField(
        'MontoTotalOtraMoneda',
        null=False,
    )


class OtherCurrencyDetailForm(Form):
    price_other_currency = DecimalField(
        'PrecioOtraMoneda',
        null=False,
    )
    discount_other_currency = DecimalField(
        'DescuentoOtraMoneda',
    )
    surcharge_another_currency = DecimalField(
        'RecargoOtraMoneda',
    )
    amount_item_other_currency = DecimalField(
        'MontoItemOtraMoneda',
        null=False,
    )


class ItemCodeForm(Form):
    code_type = StrField(
        'TipoCodigo',
        max_length=14,
    )
    item_code = StrField(
        'CodigoItem',
        max_length=35,
    )


class RetentionForm(Form):
    indicator_agent_withholding_perception = IntField(
        'IndicadorAgenteRetencionoPercepcion',
        min_value=1,
        max_value=2,
    )
    itbis_amount_withheld = DecimalField(
        'MontoITBISRetenido',
    )
    isr_amount_withheld = DecimalField(
        'MontoISRRetenido',
    )


class SubquantityForm(Form):
    subquantity = DecimalField(
        'Subcantidad',
        max_digits=19,
        decimal_places=3,
    )
    code_subquantity = UnitMeasureField(
        'CodigoSubcantidad',
    )


class SubDiscountForm(Form):
    sub_discount_rate = StrField(
        'TipoSubDescuento',
        max_length=1,
        choices=['%', '$'],
    )
    sub_discount_percentage = DecimalField(
        'SubDescuentoPorcentaje',
        max_value=999.99,
    )
    sub_discount_amount = DecimalField(
        'MontoSubDescuento',
    )


class SubSurchargeForm(Form):
    sub_surcharge_type = StrField(
        'TipoSubRecargo',
        max_length=1,
        choices=['%', '$'],
    )
    sub_surcharge_percentage = DecimalField(
        'SubRecargoPorcentaje',
        max_value=999.99,
    )
    sub_surcharge_amount = DecimalField(
        'MontoSubRecargo',
    )


class TaxForm(Form):
    tax_type = IntField(
        'TipoImpuesto',
        max_value=999,
        validators=[
            validate_tax_type,
        ]
    )
    additional_tax_rate = DecimalField(
        'TasaImpuestoAdicional',
        max_value=999.99,
    )
    selective_tax_amount_specific_consumption = DecimalField(
        'MontoImpuestoSelectivoConsumoEspecifico',
    )
    amount_selective_consumption_tax_advalorem = DecimalField(
        'MontoImpuestoSelectivoConsumoAdvalorem',
    )
    other_additional_taxes = DecimalField(
        'OtrosImpuestosAdicionales',
    )


class ItemDetailForm(Form):
    line_number: int = IntField(
        'NumeroLinea',
        null=False,
    )
    item_code_table: List[ItemCodeForm] = ListFormField(
        'TablaCodigosItem',
        form_class=ItemCodeForm,
        max_length=5,
    )
    billing_indicator: int = IntField(
        'IndicadorFacturacion',
        null=False,
        max_value=4,
        validators=[
            validate_item_billing_indicator,
        ]
    )
    retention: RetentionForm = FormField(
        'Retencion',
        form_class=RetentionForm,
    )
    item_name: str = StrField(
        'NombreItem',
        null=False,
        max_length=80,
    )
    good_service_indicator: int = IntField(
        'IndicadorBienoServicio',
        null=False,
        min_value=1,
        max_value=2,
        validators=[
            validate_item_good_service_indicator,
        ]
    )
    item_description: str = StrField(
        'DescripcionItem',
        max_length=1000,
    )
    quantity_item: Decimal = DecimalField(
        'CantidadItem',
        null=False,
    )
    unit_measure: int = UnitMeasureField(
        'UnidadMedida',
    )
    quantity_reference: Decimal = DecimalField(
        'CantidadReferencia',
    )
    reference_unit: int = UnitMeasureField(
        'UnidadReferencia',
    )
    subquantity_table: List[SubquantityForm] = ListFormField(
        'TablaSubcantidad',
        form_class=SubquantityForm,
        max_length=5,
    )
    degrees_alcohol: Decimal = DecimalField(
        'GradosAlcohol',
        max_value=999.99,
    )
    unit_price_reference: Decimal = DecimalField(
        'PrecioUnitarioReferencia',
    )
    elaboration_date: datetime.date = DateField(
        'FechaElaboracion',
    )
    expiration_date_item: datetime.date = DateField(
        'FechaVencimientoItem',
    )
    unit_price_item: Decimal = DecimalField(
        'PrecioUnitarioItem',
        null=False,
        max_digits=20,
        decimal_places=4,
    )
    discount_amount: Decimal = DecimalField(
        'DescuentoMonto',
    )
    sub_discounts: List[SubDiscountForm] = ListFormField(
        'TablaSubDescuento',
        form_class=SubDiscountForm,
        max_length=12,
    )
    surcharge_amount: Decimal = DecimalField(
        'RecargoMonto',
    )
    sub_surcharge: List[SubSurchargeForm] = ListFormField(
        'TablaSubRecargo',
        form_class=SubSurchargeForm,
        max_length=12,
    )
    additional_taxes: List[TaxForm] = ListFormField(
        'TablaImpuestoAdicional',
        form_class=TaxForm,
        max_length=2,
    )
    other_currency_detail: OtherCurrencyDetailForm = FormField(
        'TablaSubcantidad',
        form_class=OtherCurrencyDetailForm,
    )
    item_amount: Decimal = DecimalField(
        'MontoItem',
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_amount = self.get_item_amount()

    def get_item_amount(self) -> Decimal:
        """Obtiene (Precio Unitario * Cantidad) - Monto Descuento + Monto Recargo."""
        return (
            self.get_item_amount_without_discount() -
            (
                (self.discount_amount or 0) +
                (self.surcharge_amount or 0)
            )
        )

    def get_item_amount_without_discount(self) -> Decimal:
        """Obtiene (Precio Unitario * Cantidad)."""
        return self.unit_price_item * self.quantity_item



class SubtotalForm(Form):
    sub_total_number = IntField(
        'NumeroSubTotal',
        min_value=1,
        max_value=20, # Porque solo se pueden incluir 20 repeticiones en la tabla <Subtotales>
    )
    subtotal_description = StrField(
        'DescripcionSubtotal',
        max_length=40,
    )
    order = IntField(
        'Order',
        max_value=99,
    )
    sub_total_amount_taxed_total = DecimalField(
        'SubTotalMontoGravadoTotal',
    )
    sub_total_amount_taxed_i1 = DecimalField(
        'SubTotalMontoGravadoI1'
    )
    sub_total_amount_taxed_i2 = DecimalField(
        'SubTotalMontoGravadoI2',
    )
    sub_total_amount_taxed_i3 = DecimalField(
        'SubTotalMontoGravadoI3',
    )
    # Campo es calculado.
    itbis_sub_total = DecimalField(
        'SubTotaITBIS',
        editable=False,
    )
    itbis_1_sub_total = DecimalField(
        'SubTotaITBIS1',
    )
    itbis_2_sub_total = DecimalField(
        'SubTotaITBIS2',
    )
    itbis_3_sub_total = DecimalField(
        'SubTotaITBIS3',
    )
    sub_total_additional_tax = DecimalField(
        'SubTotalImpuestoAdicional',
    )
    sub_total_exempt = DecimalField(
        'SubTotalExento',
    )
    # Campo calculado.
    sub_total_amount = DecimalField(
        'MontoSubTotal',
        editable=False,
    )
    lines = IntField(
        'Lineas',
        max_value=99,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.itbis_sub_total = sum((
            self.itbis_1_sub_total or 0,
            self.itbis_2_sub_total or 0,
            self.itbis_3_sub_total or 0
        ))
        self.sub_total_amount = sum((
            self.sub_total_amount_taxed_total or 0,
            self.itbis_sub_total or 0,
            self.sub_total_additional_tax or 0,
            self.sub_total_exempt or 0
        ))


class DiscountsOrSurchargeForm(Form):
    """
    Descuento o recargo.
    """
    line_number = IntField(
        'NumeroLinea',
        min_value=1,
        max_value=20,
    )
    fit_type = StrField(
        'TipoAjuste',
        min_length=1,
        max_length=1,
        choices=FIT_TYPES,
        validators=[
            validate_fit_type,
        ]
    )
    norma_1007_indicator = IntField(
        'IndicadorNorma1007',
        max_value=1,
    )
    description_discount_or_surcharge = StrField(
        'DescripcionDescuentooRecargo',
        max_length=45,
    )
    type_value = StrField(
        'TipoValor',
        max_length=1,
        choices=['%', '$'],
    )
    discount_value_or_surcharge = DecimalField(
        'ValorDescuentooRecargo',
        max_value=999.99,
    )
    discount_amount_or_surcharge = DecimalField(
        'MontoDescuentooRecargo',
    )
    discount_amount_or_surcharge_other_currency = DecimalField(
        'MontoDescuentooRecargoOtraMoneda',
    )
    indicator_billing_discount_or_surcharge = IntField(
        'IndicadorFacturacionDescuentooRecargo',
        max_value=4,
        validators=[
            validate_item_billing_indicator
        ],
    )


class SubtotalAdditionalTaxForm(Form):
    subtotal_selective_tax_for_specific_consumption_page = DecimalField(
        'SubtotalImpuestoSelectivoConsumoEspecificoPagina',
    )
    subtotal_other_tax = DecimalField(
        'SubtotalOtrosImpuesto',
    )


class PaginationForm(Form):
    """
    En esta sección se indica la cantidad de páginas del e-CF en la
    Representación Impresa y cuales ítems estarán en cada una. Cada objeto
    deberá repetirse para el total de páginas especificadas. La sección
    paginación es condicional a que el e-CF contenga más de una página, es
    decir, si la RI contiene una sola página, no debe enviarse.

    Campo DGII <Paginacion>
    """
    page_no = IntField(
        'PaginaNo',
        min_value=1,
        max_value=100,
    )
    no_line_from = IntField(
        'NoLineaDesde',
        min_value=1,
        max_value=999,
    )
    no_line_until = IntField(
        'NoLineaHasta',
        min_value=1,
        max_value=999,
    )
    subtotal_amount_taxed_page = DecimalField('SubtotalMontoGravadoPagina')
    subtotal_amount_taxed_1_page = DecimalField('SubtotalMontoGravado1Pagina')
    subtotal_amount_taxed_2_page = DecimalField('SubtotalMontoGravado2Pagina')
    subtotal_amount_taxed_3_page = DecimalField('SubtotalMontoGravado3Pagina')
    exempt_subtotal_page = DecimalField('SubtotalExentoPagina')
    itbis_subtotal_page = DecimalField('SubtotalItbisPagina')
    itbis_1_subtotal_page = DecimalField('SubtotalItbis1Pagina')
    itbis_2_subtotal_page = DecimalField('SubtotalItbis2Pagina')
    itbis_3_subtotal_page = DecimalField('SubtotalItbis3Pagina')
    subtotal_additional_tax_page = DecimalField('SubtotalImpuestoAdicionalPagina')
    subtotal_additional_tax = FormField(
        'SubtotalImpuestoAdicional',
        form_class=SubtotalAdditionalTaxForm,
    )
    subtotal_amount_page = DecimalField('MontoSubtotalPagina')
    subtotal_non_billable_amount_page = DecimalField('SubtotalMontoNoFacturablePagina')

    def validate(self, data: dict):
        no_line_from = data.get('no_line_from')
        no_line_until = data.get('no_line_until')
        if no_line_from is not None and no_line_until is not None:
            if no_line_from > no_line_until:
                raise ValidationError('El valor de no_line_from debe ser igual o menor a no_line_until.')
        return data


class InformationReferenceForm(Form):
    """
    Información de referencia.
    <InformacionReferencia>
    """
    ncf_modified = NCFField(
        'NCFModificado',
    )
    rnc_other_taxpayer = RNCField(
        'RNCOtroContribuyente',
    )
    ncf_modified_date = DateField(
        'FechaNCFModificado',
    )
    modification_code = IntField(
        'CodigoModificacion',
        min_value=1,
        max_value=5,
        validators=[
            validate_modification_code,
        ]
    )
    reason_for_modification = StrField(
        'RazonModificacion',
        max_length=90,
    )


class PdfForm(Form):
    type = StrField(max_length=7, default='generic')
    note = StrField()


class ConfigForm(Form):
    """
    Configuración adicional del documento electrónico
    """
    pdf = FormField(dgii_name=None, form_class=PdfForm, default=PdfForm())



class InvoiceForm(Form):
    """
    Factura Electrónica.

    Args:
    * `company_id` (str): Identificador de la empresa.
    * `id_doc` (IdDocForm): Documento de identificación.
    * `sender` (SenderForm): Formulario del remitente.
    * `buyer` (BuyerForm): Formulario del comprador.
    * `additional_information` (AdditionalInformationForm, opcional): Información adicional.
    * `transport` (TransportForm, opcional): Formulario de transporte.
    * `totals` (TotalsForm): Formulario de totales.
    * `other_currency` (OtherCurrencyForm, opcional): Formulario de otra moneda.
    * `item_details` (List[ItemDetailForm]): Detalles de los elementos.
    * `subtotals` (List[SubtotalForm], opcional): Subtotales.
    * `discounts_or_surcharges` (List[DiscountsOrSurchargeForm], opcional): Descuentos o recargos.
    * `pagination` (List[PaginationForm], opcional): Paginación.
    * `information_reference` (InformationReferenceForm, opcional): Información de referencia.
    * `config` (ConfigForm, opcional): Configuración.
    """
    company_id: str = StrField(
        null=False,
    )
    id_doc: IdDocForm = FormField(
        'IdDoc',
        null=False,
        form_class=IdDocForm,
    )
    sender: SenderForm = FormField(
        'Emisor',
        null=False,
        form_class=SenderForm,
    )
    buyer: BuyerForm = FormField(
        'Comprador',
        null=False,
        form_class=BuyerForm,
    )
    additional_information: AdditionalInformationForm = FormField(
        'InformacionesAdicionales',
        form_class=AdditionalInformationForm,
    )
    transport: TransportForm = FormField(
        'Transporte',
        form_class=TransportForm,
    )
    totals: TotalsForm = FormField(
        'Totales',
        null=False,
        form_class=TotalsForm,
    )
    other_currency: OtherCurrencyForm = FormField(
        'OtraMoneda',
        form_class=OtherCurrencyForm,
    )
    item_details: List[ItemDetailForm] = ListFormField(
        'DetallesItem',
        null=False,
        form_class=ItemDetailForm,
        max_length=100,
    )
    subtotals: List[SubtotalForm] = ListFormField(
        'Subtotales',
        form_class=SubtotalForm,
        max_length=20,
    )
    discounts_or_surcharges: List[DiscountsOrSurchargeForm] = ListFormField(
        'DescuentosORecargos',
        form_class=DiscountsOrSurchargeForm,
        max_length=20,
    )
    pagination: List[PaginationForm] = ListFormField(
        'Paginacion',
        form_class=PaginationForm,
        max_length=100,
    )
    information_reference: InformationReferenceForm = FormField(
        'InformacionReferencia',
        form_class=InformationReferenceForm,
    )
    config = FormField(
        dgii_name=None,
        form_class=ConfigForm,
        default=ConfigForm(),
    )

    def validate(self, data):
        data = super().validate(data)

        ncf_serie, ncf_code, ncf_sequence = split_ncf(self.id_doc.encf)

        # El RNC del comprador es opcional para algunos tipos de NCF.
        if not self.buyer.rnc and ncf_code in (NCF_E_31, NCF_E_41, NCF_E_45):
            raise ValidationError(
                'El RNC del comprobador es obligatorio para los tipos de '
                'comprobantes 31, 41 y 45.'
            )

        # Validar los totals.
        # Estos comprobantes no aplican para itbis.
        if split_ncf(data['id_doc'].encf)[1] in (NCF_E_43, NCF_E_44, NCF_E_47):
            if (
                self.totals.total_taxed_amount or
                self.totals.i1_amount_taxed or
                self.totals.i2_amount_taxed or
                self.totals.i3_amount_taxed or
                self.totals.itbis_total or
                self.totals.itbis1_total or
                self.totals.itbis2_total or
                self.totals.itbis3_total or
                self.totals.total_taxed_amount
            ):
                raise ValidationError(
                    f'Los tipos de NCF {NCF_E_43}, {NCF_E_44} y {NCF_E_47} no aplican para itbis.'
                )

        # Validar que coincidan los montos con los totales calculados.

        # Total de la suma de valores de Ítems gravados asignados a ITBIS tasa 1
        # (tasa 18%), menos descuentos más recargos. 12 Condicional a que en la
        # línea de detalle exista algún ítem gravado a tasa ITBIS1.
        if self.totals.i1_amount_taxed:
            if not compare_amounts_with_margin(self.totals.i1_amount_taxed, self.items_i1_amount):
                raise ValidationError(
                    f'El campo {self.totals.i1_amount_taxed=} no coincide con '
                    'la sumatoria de los valores del detalle gravado con tasa '
                    f'{ITEM_BILLING_INDICATORS[ITEM_BILLING_INDICATOR_1]} '
                    f'menos descuentos mas recargos {self.items_i1_amount=}'
                )
        # Total de la suma de valores de Ítems gravados asignados a ITBIS tasa 2
        # (tasa 16%), menos descuentos más recargos. Condicional a que en la
        # línea de detalle exista algún ítem gravado a tasa ITBIS2.
        if self.totals.i2_amount_taxed:
            if not compare_amounts_with_margin(self.totals.i2_amount_taxed, self.items_i2_amount):
                raise ValidationError(
                    f'El campo {self.totals.i2_amount_taxed=} no coincide con '
                    'la sumatoria de los valores del detalle gravado con tasa '
                    f'{ITEM_BILLING_INDICATORS[ITEM_BILLING_INDICATOR_2]} '
                    'menos descuentos mas recargos.'
                )
        # Total de la suma de valores de Ítems gravados asignados a ITBIS tasa 3
        # (tasa 0%), menos descuentos más recargos. Condicional a que en la
        # línea de detalle exista algún ítem gravado a tasa ITBIS3.
        if self.totals.i3_amount_taxed:
            if not compare_amounts_with_margin(self.totals.i3_amount_taxed, self.items_i3_amount):
                raise ValidationError(
                    f'El campo {self.totals.i3_amount_taxed=} no coincide con '
                    'la sumatoria de los valores del detalle gravado con tasa '
                    f'{ITEM_BILLING_INDICATORS[ITEM_BILLING_INDICATOR_3]} '
                    'menos descuentos mas recargos.'
                )
        # Total de la suma de valores de ítems exentos, menos descuentos más
        # recargos. Condicional a que en la línea de detalle exista algún ítem exento.
        if self.totals.exempt_amount:
            if not compare_amounts_with_margin(self.totals.exempt_amount, self.items_exempt_amount):
                raise ValidationError(
                    f'El campo {self.totals.exempt_amount=} no coincide con '
                    'la sumatoria de los valores del detalle gravado con tasa '
                    f'{ITEM_BILLING_INDICATORS[ITEM_BILLING_INDICATOR_4]} '
                    'menos descuentos mas recargos.'
                )

        return data

    @property
    def items_amount(self):
        """Sumatoria de `item_amount` para cada item en `item_details`."""
        return sum([(e.item_amount or 0) for e in self.item_details])

    @property
    def items_i1_amount(self):
        """Monto total gravado con `ITEM_BILLING_INDICATOR_1`"""
        return sum([
            (e.item_amount or 0) for e in self.item_details
            if e.billing_indicator == ITEM_BILLING_INDICATOR_1
        ])

    @property
    def items_i2_amount(self):
        """Monto total gravado con `ITEM_BILLING_INDICATOR_2`"""
        return sum([
            (e.item_amount or 0) for e in self.item_details
            if e.billing_indicator == ITEM_BILLING_INDICATOR_2
        ])

    @property
    def items_i3_amount(self):
        """Monto total gravado con `ITEM_BILLING_INDICATOR_3`"""
        return sum([
            (e.item_amount or 0) for e in self.item_details
            if e.billing_indicator == ITEM_BILLING_INDICATOR_3
        ])

    @property
    def items_exempt_amount(self):
        """Monto total gravado con `ITEM_BILLING_INDICATOR_4` (excento)"""
        return sum([
            (e.item_amount or 0) for e in self.item_details
            if e.billing_indicator == ITEM_BILLING_INDICATOR_4
        ])



class CreditNoteIdDocForm(IdDocForm):
    """
    idDoc Form para CreditNoteForm.

    Args:
    * `company_id` (str): Identificador de la empresa.
    * `id_doc` (IdDocForm): Documento de identificación.
    * `sender` (SenderForm): Formulario del remitente.
    * `buyer` (BuyerForm): Formulario del comprador.
    * `additional_information` (AdditionalInformationForm, opcional): Información adicional.
    * `transport` (TransportForm, opcional): Formulario de transporte.
    * `totals` (TotalsForm): Formulario de totales.
    * `other_currency` (OtherCurrencyForm, opcional): Formulario de otra moneda.
    * `item_details` (List[ItemDetailForm]): Detalles de los elementos.
    * `subtotals` (List[SubtotalForm], opcional): Subtotales.
    * `discounts_or_surcharges` (List[DiscountsOrSurchargeForm], opcional): Descuentos o recargos.
    * `pagination` (List[PaginationForm], opcional): Paginación.
    * `information_reference` (InformationReferenceForm, opcional): Información de referencia.
    * `config` (ConfigForm, opcional): Configuración.
    * `encf` (str):
    * `deferred_delivery_indicator` (int):
    * `tax_amount_indicator` (int):
    * `income_type` (int):
    * `payment_type` (int):
    * `payment_deadline` (datetime.date):
    * `date_from` (datetime.date):
    * `date_until` (datetime.date):
    * `total_pages` (int):
    * `credit_note_indicator` (int):
    """
    sequence_due_date = None
    payment_term = None
    payment_forms_table = None
    payment_account_type = None
    payment_account_number = None
    bank_payment = None
    credit_note_indicator: int = IntField(
        'IndicadorNotaCredito',
        null=False,
        min_value=0,
        max_value=1,
        help_text=(
            'Sólo para Notas de Crédito que no tienen derecho a rebajar ITBIS. '
            'El indicador tomará valor 1 si la fecha es mayor a 30 días '
            'calendario de la emisión del e-CF afectado.'
        )
    )

    def validate(self, data):
        data = super().validate(data)

        # FIXME: Pendiente de validación esto:
        # Sólo para Notas de Crédito que no tienen derecho a rebajar
        # ITBIS.El indicador tomará valor 1 si la fecha es mayor a 30 días
        # calendario de la emisión del e-CF afectado.
        # https://dgii.gov.do/cicloContribuyente/facturacion/comprobantesFiscalesElectronicosE-CF/Documentacin%20sobre%20eCF/Formatos%20XML/Formato%20Comprobante%20Fiscal%20Electr%C3%B3nico%20(e-CF)%20v1.0.pdf
        logging.warning('Pendiente validar credit_note_indicator.')

        return data


class CreditNoteForm(InvoiceForm):
    """
    Nota de Crédito Electrónica (34).

    https://developer.alanube.co/v1.0-DOM/reference/createcreditnotes
    """
    id_doc: CreditNoteIdDocForm = FormField(
        'IdDoc',
        null=False,
        form_class=CreditNoteIdDocForm,
    )


class CancellationHeaderForm(Form):
    rnc_sender = RNCField(
        'RncEmisor',
        null=False,
    )
    cancelled_encf_quantity = IntField(
        'CantidadeNCFAnulados',
        null=False,
        min_value=1,
        max_value=9999999999,
    )


class CancellationItemRangeCancelledEnfcForm(Form):
    """
    Tabla que contiene un rango de las secuencias anuladas de manera consecutiva,
    de acuerdo con el tipo de e-CF. Se pueden incluir hasta 10,000 repeticiones.
    """
    dgii_name = 'TablaRangoSecuenciasAnuladaseNCF'

    encf_from = NCFField(
        'SecuenciaeNCFDesde',
        null=False,
        help_text=(
            'Se refiere al Número de Comprobante Fiscal Electrónico (e-NCF) '
            'con el secuencial que inicia el rango de secuencias que será anulado.'
        )
    )
    encf_until = NCFField(
        'SecuenciaeNCFHasta',
        null=False,
        help_text=(
            'Se refiere al Número de Comprobante Fiscal Electrónico (e-NCF) con '
            'el secuencial que finaliza el rango de secuencias que será anulado.'
        )
    )


class CancellationItemForm(Form):
    """
    Anulación se pueden incluir 10 hasta repeticiones.
    """
    dgii_name = 'Anulacion'

    line_number = IntField(
        'NoLinea',
        null=False,
        min_value=1,
        max_value=10,
        help_text='Número de la línea o secuencial. Desde 1 hasta 10 repeticiones.',
    )
    ecf_type = IntField(
        'TipoeCF',
        null=False,
        min_value=31,
        max_value=47,
        choices=[int(code) for code in NCF_SERIES[NCF_E]['codes']],
        help_text='Tipo Comprobante Fiscal Electrónico (e-CF).',
    )
    range_cancelled_enfc = ListFormField(
        'TablaRangoSecuenciasAnuladaseNCF',
        null=False,
        form_class=CancellationItemRangeCancelledEnfcForm,
        max_length=10000,
        help_text=(
            'Tabla que contiene un rango de las secuencias anuladas de manera '
            'consecutiva, de acuerdo con el tipo de e-CF. Se pueden incluir '
            'hasta 10,000 repeticiones.'
        )
    )
    cancelled_encf_quantity = IntField(
        'CantidadeNCFAnulados',
        null=False,
        min_value=1,
        max_value=9999999999,
        help_text=(
            'Cantidad de secuencias de e- NCF que se está anulando. En este '
            'campo se deberá sumar las secuencias colocados en la tabla de '
            'rangos de secuencias anuladas de e-NCF'
        )
    )


class CancellationForm(Form):
    """
    Sirve para emitir anulaciones,
    las cuales se usan para anular rangos de numeración que no se usarán.

    ¿Qué se puede anular?
    ---------------------
        1. Comprobantes que han sido rechazados.

    https://developer.alanube.co/v1.0-DOM/reference/createcancelations
    """

    header = FormField(
        'Encabezado',
        null=False,
        form_class=CancellationHeaderForm,
    )
    cancellations = ListFormField(
        'Anulacion',
        null=False,
        max_length=10,
        form_class=CancellationItemForm,
    )