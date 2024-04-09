with
  cte_invoice as (
    select
      id as invoice_id, 
      status
    from
      invoice
    where
      customer_id = '9ca4743f-5c9e-46e3-a2db-1d484405d5ad'
      and issued_at = '2024-04-02'
      and status = 'FINALIZED'
  ),
  cte_line_item as (
    select
      li.name as li_name,
      li.id as li_id 
    from
      line_item li 
      join cte_invoice ci on li.invoice_id = ci.invoice_id
  )
select
  li_name as "SKU",
  sli.name as "Description",
  sli.quantity as "Quantity",
  '$' || to_char(sli.subtotal / sli.quantity, 'FM999,999,999,999.99') as "Unit Price",
  '$' || to_char(sli.subtotal, 'FM999,999,999,999.99') as "Total"
from
  sub_line_item sli
  join cte_line_item li on li.li_id = sli.line_item_id
order by
  sli.name;

-- This one was the most complex but also the most straightforward in terms of the requirements. 
-- If this was a business case, this is the query I'd write, and I would format by SKU -> line item on the invoice.
-- I used two CTEs here - one for invoice and one for line item based on the invoice. 
-- Then I just joined that on the sub line item for the final output. 
-- The only question I had here was the numerical values - I saw in the table much of the pricing was in cents USD
-- But the consumption was so high, the unit price ended up being similar even without converting from cents. 
-- More of a business question than anything. 