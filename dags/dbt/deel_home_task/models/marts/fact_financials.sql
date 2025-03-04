with normalized as (
    select
        inv.organization_id
        ,created_at::date as invoice_created_at
        ,case
            when status not in ('failed','unpayable','cancelled','skipped','processing') 
            then (amount*fx_rate)::decimal(15,2)
            else 0
        end as invoice_amount
        ,case
            when status = 'paid'
            then (payment_amount*fx_rate_payment)::decimal(15,2)
            else 0
        end as usd_payment
        
    from {{ ref('stg_invoices') }} as inv
    left join {{ ref('stg_organizations') }} as org using(ORGANIZATION_ID)
)

,balance as (
    select
        organization_id
        ,invoice_created_at
        ,sum(invoice_amount) as total_amount
        ,sum(usd_payment) as total_payment
        ,sum(total_amount - total_payment) over(partition by organization_id order by invoice_created_at asc) as current_balance
    from normalized
    group by all
)

select
    organization_id
    ,invoice_created_at
    ,current_balance
    ,lag(current_balance) over (partition by organization_id order by invoice_created_at asc) as last_day_balance
    ,case
        when DIV0NULL(last_day_balance,current_balance)*100 <= 50 then 1
        else 0
    end as send_alert
from balance