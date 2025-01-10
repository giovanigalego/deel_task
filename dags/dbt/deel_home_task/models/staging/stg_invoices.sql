with invoices as (
    select * from {{ source('raw', 'raw_invoices') }}
)

select
    INVOICE_ID
    ,PARENT_INVOICE_ID
    ,TRANSACTION_ID
    ,ORGANIZATION_ID
    ,TYPE
    ,upper(STATUS) as STATUS
    ,CURRENCY
    ,PAYMENT_CURRENCY
    ,PAYMENT_METHOD
    ,AMOUNT
    ,PAYMENT_AMOUNT
    ,FX_RATE
    ,FX_RATE_PAYMENT
from invoices