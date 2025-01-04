from .api import AlanubeAPI


def create_company(payload):
    """
    Dar de alta a una empresa
    """
    return AlanubeAPI.create_company(payload)


def update_company(payload, company_id: str = None):
    """
    Actualiza la información de una empresa
    """
    return AlanubeAPI.update_company(payload, company_id)


def get_company(company_id: str = None):
    """
    Consultar la información de una empresa
    """
    return AlanubeAPI.get_company(company_id)


def send_fiscal_invoice(payload):
    """
    Emitir Factura de Crédito Fiscal Electrónica (31)
    """
    return AlanubeAPI.send_fiscal_invoice(payload)


def get_fiscal_invoice_status(document_id: str, company_id: str = None):
    """
    Consultar el estado de la Factura de Crédito Fiscal Electrónica (31)
    """
    return AlanubeAPI.get_fiscal_invoice_status(document_id, company_id)


def send_invoice(payload):
    """
    Emitir Factura de Consumo Electrónica (32)
    """
    return AlanubeAPI.send_invoice(payload)


def get_invoice_status(document_id: str, company_id: str = None):
    """
    Consultar el estado de la Factura de Consumo Electrónica (32)
    """
    return AlanubeAPI.get_invoice_status(document_id, company_id)


def send_debit_note(payload):
    """
    Emitir Nota de Débito Electrónica (33)
    """
    return AlanubeAPI.send_debit_note(payload)


def get_debit_note_status(document_id: str, company_id: str = None):
    """
    Consultar el estado de la Nota de Débito Electrónica (33)
    """
    return AlanubeAPI.get_debit_note_status(document_id, company_id)


def send_credit_note(payload):
    """
    Emitir Nota de Crédito Electrónica (34)
    """
    return AlanubeAPI.send_credit_note(payload)


def get_credit_note_status(document_id: str, company_id: str = None):
    """
    Consultar el estado de la Nota de Crédito Electrónica (34)
    """
    return AlanubeAPI.get_credit_note_status(document_id, company_id)


def send_purchase(payload):
    """
    Emitir Documento de Compra Electrónico (41)
    """
    return AlanubeAPI.send_purchase(payload)


def get_purchase_status(document_id: str, company_id: str = None):
    """
    Consultar el estado del Documento de Compra Electrónico (41)
    """
    return AlanubeAPI.get_purchase_status(document_id, company_id)


def send_minor_expense(payload):
    """
    Emitir Documento de Gasto Menor Electrónico (43)
    """
    return AlanubeAPI.send_minor_expense(payload)


def get_minor_expense_status(document_id: str, company_id: str = None):
    """
    Consultar el estado del Documento de Gasto Menor Electrónico (43)
    """
    return AlanubeAPI.get_minor_expense_status(document_id, company_id)


def send_special_regime(payload):
    """
    Emitir Documento de Régimen Especial Electrónico (44)
    """
    return AlanubeAPI.send_special_regime(payload)


def get_special_regime_status(document_id: str, company_id: str = None):
    """
    Consultar el estado del Documento de Régimen Especial Electrónico (44)
    """
    return AlanubeAPI.get_special_regime_status(document_id, company_id)


def send_gubernamental(payload):
    """
    Emitir Documento Gubernamental Electrónico (45)
    """
    return AlanubeAPI.send_gubernamental(payload)


def get_gubernamental_status(document_id: str, company_id: str = None):
    """
    Consultar el estado del Documento Gubernamental Electrónico (45)
    """
    return AlanubeAPI.get_gubernamental_status(document_id, company_id)


def send_export_support(payload):
    """
    Emitir Documento de Soporte de Exportación Electrónico (46)
    """
    return AlanubeAPI.send_export_support(payload)


def get_export_support_status(document_id: str, company_id: str = None):
    """
    Consultar el estado del Documento de Soporte de Exportación Electrónico (46)
    """
    return AlanubeAPI.get_export_support_status(document_id, company_id)


def send_payment_abroad_support(payload):
    """
    Emitir Documento de Soporte de Pagos al Exterior Electrónico (47)
    """
    return AlanubeAPI.send_payment_abroad_support(payload)


def get_payment_abroad_support_status(document_id: str, company_id: str = None):
    """
    Consultar el estado del Documento de Soporte de Pagos al Exterior Electrónico (47)
    """
    return AlanubeAPI.get_payment_abroad_support_status(document_id, company_id)


def send_cancellation(payload):
    """
    Emitir anulación de numeración
    """
    return AlanubeAPI.send_cancellation(payload)


def get_cancellation_status(cancellation_id: str, company_id: str = None):
    """
    Consultar el estado de la anulación
    """
    return AlanubeAPI.get_cancellation_status(cancellation_id, company_id)


def get_received_document(received_document_id: str, company_id: str = None):
    """
    Consultar un 'documento recibido'
    """
    return AlanubeAPI.get_received_document(received_document_id, company_id)


def get_received_documents(
    company_id=None,
    limit=25,
    page=1,
    start=None,
    end=None,
):
    """
    Consultar un 'documento recibido'
    """
    return AlanubeAPI.get_received_documents(company_id, limit, page, start, end)
