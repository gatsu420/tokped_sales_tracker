# counts daily product view lift  

with raw_count as
(select
    date(inserted_time) as tanggal,
    cast(view_count as signed) as view_count
from recent_update
join (select @cum_sum := 0) qq

# sample product link
where product_link = "https://www.tokopedia.com/bukapetshop/bolt-cat-1kg-repack-makanan-kucing-murah-ikan"
and hour(inserted_time) = 0),

diff_count as
(select 
    *,
    view_count - lag(view_count, 1) over 
        (order by tanggal) as view_count_lift
from raw_count)

select * from diff_count
where view_count_lift is not null