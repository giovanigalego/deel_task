with parent_invoice as (
    select
        invoice_id
        ,parent_invoice_id
        ,(payment_amount*fx_rate_payment) as parent_usd_payment
    from {{ ref('stg_invoices') }}
    where
        status = 'paid'
)

select
    invoice.organization_id
    ,invoice.payment_currency
    ,avg(parent.parent_usd_payment/(invoice.payment_amount * invoice.fx_rate_payment)) as percent
from {{ ref('stg_invoices') }} as invoice
inner join parent_invoice as parent on invoice.invoice_id = parent.parent_invoice_id 
group by all