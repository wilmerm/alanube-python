from typing import Dict, TypedDict, List, Literal


class Metadata(TypedDict):
    current_page: int
    limit: int
    from_: int
    to: int


class DGIIResponse(TypedDict):
    valor: str
    codigo: int


class GovernmentResponse(TypedDict):
    value: List[DGIIResponse]
    code: int


class DocumentResponse(TypedDict):
    id: str
    stampDate: str
    status: Literal[
        "REGISTERED",
        "TO_SEND",
        "FAILED",
        "WAITING_RESPONSE",
        "TO_NOTIFY",
        "FINISHED"
    ]
    legalStatus: Literal[
        "NOT_FOUND",
        "IN_PROCESS",
        "ACCEPTED",
        "ACCEPTED_WITH_OBSERVATIONS",
        "REJECTED"
    ]
    companyIdentification: str
    trackId: str
    documentNumber: str
    sequenceConsumed: bool
    signatureDate: str
    securityCode: str
    documentStampUrl: str
    xml: str
    pdf: str
    governmentResponse: GovernmentResponse


class ListDocumentResponse(TypedDict):
    metadata: Metadata
    documents: List[DocumentResponse]


class ReceivedDocumentsResponse(TypedDict):
    id: str
    issuerIdentification: str
    buyerIdentification: str
    documentType: str
    documentNumber: str
    documentStampDate: str
    signatureDateTime: str
    totalAmount: str
    status: str
    errorMsg: str
    commercialResponse: str
    timestamp: str


class ListReceivedDocumentsResponse(TypedDict):
    metadata: Metadata
    documents: List[ReceivedDocumentsResponse]


class ReportCompaniesDocumentsTotalData(TypedDict):
    totalEmittedDocuments: int
    fiscalInvoices: int
    invoices: int
    creditNotes: int
    debitNotes: int
    exportSupports: int
    gubernamentals: int
    minorExpenses: int
    paymentAbroadSupports: int
    purchases: int
    specialRegimes: int


class ReportCompaniesDocumentsTotalResponse(TypedDict):
    data: ReportCompaniesDocumentsTotalData


Companies = Dict[str, ReportCompaniesDocumentsTotalData] # El key es el company_id


class ReportUsersDocumentsTotalData(TypedDict):
    totalEmittedDocuments: int
    companies: Dict[str, ReportCompaniesDocumentsTotalData]


class ReportUsersDocumentsTotalResponse(TypedDict):
    data: ReportUsersDocumentsTotalData


class MonthlyQuantity(TypedDict):
    year: int
    month: int
    quantity: int


class ReportDocumentsStatsMonthly(TypedDict):
    totalEmittedDocuments: List[MonthlyQuantity]
    fiscalInvoices: List[MonthlyQuantity]
    invoices: List[MonthlyQuantity]
    creditNotes: List[MonthlyQuantity]
    debitNotes: List[MonthlyQuantity]
    exportSupports: List[MonthlyQuantity]
    gubernamentals: List[MonthlyQuantity]
    minorExpenses: List[MonthlyQuantity]
    paymentAbroadSupports: List[MonthlyQuantity]
    purchases: List[MonthlyQuantity]
    specialRegimes: List[MonthlyQuantity]


class DailyQuantity(TypedDict):
    month: int
    day: int
    quantity: int


class ReportDocumentsStatsDaily(TypedDict):
    totalEmittedDocuments: List[DailyQuantity]
    fiscalInvoices: List[DailyQuantity]
    invoices: List[DailyQuantity]
    creditNotes: List[DailyQuantity]
    debitNotes: List[DailyQuantity]
    exportSupports: List[DailyQuantity]
    gubernamentals: List[DailyQuantity]
    minorExpenses: List[DailyQuantity]
    paymentAbroadSupports: List[DailyQuantity]
    purchases: List[DailyQuantity]
    specialRegimes: List[DailyQuantity]
