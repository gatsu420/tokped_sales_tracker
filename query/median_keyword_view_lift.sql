# counts daily median product view lift of selected keywords

with count_raw as
(select
    date(recent_update.inserted_time) as tanggal,
    recent_update.product_link,
    keywords.keyword,
    recent_update.view_count,
    lag(date(recent_update.inserted_time), 1) over
    	(partition by recent_update.product_link
    	 order by recent_update.inserted_time) as lag_tanggal,
    lag(view_count, 1) over
    	(partition by recent_update.product_link
    	 order by recent_update.inserted_time) as lag_view_count
from recent_update
left join keywords on recent_update.keyword_id = keywords.keyword_id
where hour(recent_update.inserted_time) = 0

# invoke field filter on metabase
and {{keyword}}),

count_diff as
(select
	*,
	if(timestampdiff(day, lag_tanggal, tanggal) = 1,
		(view_count - lag_view_count),
		null) as view_lift
from count_raw),

count_median as
(select
	distinct tanggal,
	keyword,
	round(median(view_lift) over
		(partition by tanggal, keyword), 0) as median_product_view_lift
from count_diff
where view_lift is not null
order by 1, 2)

select * from count_median