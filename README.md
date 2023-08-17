# alanube-python

Python library to establish connections with the Alanube API.

## Alanube Docs

[https://developer.alanube.co/docs](https://developer.alanube.co/docs)

## Instalation

```bash
pip install alanube
```

## Use

```py
from alanube import AlanubeDGII
from alanube.dgii.forms import InvoiceForm

alanube = AlanubeDGII(token='YOUR_API_TOKEN')

id_doc = IdDocForm(
    encf='E310000000005',
    sequence_due_date: '2023-01-01',
    tax_amount_indicator: 1,
    income_type: 1,
    payment_type: 1,
    payment_deadline: '2023-01-30',
)

sender = SenderForm(
    rnc=101123456,
    company_name='My Company SRL',
    tradename='My Company',
    branch_office='Principal',
    address='Calle A, No. 1245, Santo Domingo',
    phone_number='8091234567',
    mail='mycompany@example.com',
    web_site='https://mycompany.example.com',
    seller_code='01',
    internal_invoice_number='FC0123456789',
    stamp_date='2023-01-01',
)

buyer = BuyerForm(
    rnc=101123457,
    company_name='His Company SRL',
    contact='José, Tel: 8091234567',
    mail='jose@example.com',
    address='Calle B, 1236, San Cristobal',
)

totals = TotalsForm(
    total_amount=100.00,
    total_taxed_amount=18.00,
    amount_period=118.00,
    non_billable_amount=0,
    i1_amount_taxed=0, # No Facturable
    i2_amount_taxed=100.00, # Monto gravado a ITBIS tasa1 (18%).
    i3_amount_taxed=0, # Monto gravado a ITBIS tasa1 (16%).
    exempt_amount=0, # Monto exento.
    itbis_total=18.00, # Total ITBIS
    itbis1_total=18.00, # ITBIS (18%)
    itbis2_total=0, # ITBIS (16%)
    itbis3_total=0, # ITBIS (0%)
    additional_tax_amount=None,
    additional_taxes=None,
    itbis_total_retained=None,
    itbis_total_perception=None,
    isr_total_retention=None,
    isr_total_perception=None,
)

items = [
    ItemDetailForm(
        line_number=1,
        item_code_table=None,
        billing_indicator=1,
        retention=None,
        item_name='Café Entero Paquete',
        item_description=None,
        good_service_indicator=1,
        quantity_item=10,
        unit_measure=None,
        subquantity_table=None,
        unit_price_item=100.00,
        discount_amount=0,
        sub_discounts=0,
        item_amount=1000.00,
    ),
    ...
]

config = ConfigForm()

invoice_form = invoice_form_class(
    company_id='MY_ALANUBE_COMPANY_ID',
    id_doc=id_doc,
    sender=sender,
    buyer=buyer,
    totals=totals,
    item_details=items,
    subtotals=None,
    discounts_or_surcharges=None,
    pagination=None,
    config=config,
)

response = alanube.create_invoice(invoice_form)

if response.ok:
    data = response.json()
else:
    print(response.errors)

```

## Licence

This project is licensed under the MIT License.

## Proyect Status

This project is under development

