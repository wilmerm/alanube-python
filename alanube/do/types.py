from typing import TypedDict, List, Literal


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
