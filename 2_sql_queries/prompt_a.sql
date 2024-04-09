
select
  name,
  sum(quantity) as total_quantity,
  sum(subtotal) as total_subtotal
from
  sub_line_item
where
  billable_metric_name in (
    'Images (256x256)',
    'Images (512x512)',
    'Images (1024x1024)'
  )
group by
  name;


-- As noted in the README - no rows were returned for this query when including the March 10 to March 25 timeframe (see below).
-- Manual exploration into the table showed me that all of the 'plans' 'billable metrics' and 'line items' were created in early April. 
-- I'm not sure if there was something I missed here. I originally built out a complex nested CTE to try and join billable metrics 
-- across plans and plan charge into the event, but I didn't get the results I was looking for.
-- So although this is simple, this was the closest I got. 

select
  name,
  sum(quantity) as total_quantity,
  sum(subtotal) as total_subtotal
from
  sub_line_item
where
  billable_metric_name in (
    'Images (256x256)',
    'Images (512x512)',
    'Images (1024x1024)'
  )
  and updated_at >= '2024-03-10'
  and updated_at <= '2024-03-25'
group by
  name;