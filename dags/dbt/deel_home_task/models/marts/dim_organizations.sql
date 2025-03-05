with orgs_in_invoice as (
    select
        organization_id
        ,min(created_at) as created_at
    from {{ ref('stg_invoices') }}
    group by all
)


,payments_dates as (
    select
        organization_id
        ,min(created_at) as first_payment_date
        ,max(created_at) as last_payment_date
    from {{ ref('stg_invoices') }}
    where status = 'PAID'
    group by all
)

,orgs_current_balace as (
    select
        organization_id
        ,max_by(current_balance,invoice_created_at) as current_balance
    from {{ ref('fact_financials') }}
    group by all
)


select
    orgs_invoice.organization_id
    ,pay_dates.first_payment_date
    ,pay_dates.last_payment_date
    ,org.legal_entity_country_code
    ,org.count_total_contracts_active
    ,cur_balance.current_balance
    ,ifnull(org.created_date,orgs_invoice.created_at) as created_date
    ,current_timestamp() as updated_at
from orgs_in_invoice as orgs_invoice
left join payments_dates as pay_dates using(organization_id)
left join {{ ref('stg_organizations') }} as org using(organization_id)
left join orgs_current_balace as cur_balance using(organization_id)