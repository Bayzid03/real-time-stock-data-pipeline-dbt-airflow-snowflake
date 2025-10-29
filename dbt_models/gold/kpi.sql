select
    symbol,
    current_price,
    change_amount,
    change_percent
from (
    select *,
           row_number() over (partition by symbol order by fetched_at desc) as rn
    from {{ ref('curated_stocks') }}
) t
where rn = 1
