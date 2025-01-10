with organizations as (
    select * from {{ source('raw', 'raw_organizations') }}
)

select
    ORGANIZATION_ID
    ,FIRST_PAYMENT_DATE
    ,LAST_PAYMENT_DATE
    ,LEGAL_ENTITY_COUNTRY_CODE
    ,COUNT_TOTAL_CONTRACTS_ACTIVE
    ,CREATED_DATE
from organizations