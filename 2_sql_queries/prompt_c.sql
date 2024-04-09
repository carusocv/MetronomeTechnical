select
  plan_id,
  plan_name,
  status,
  count(*) as total_invoices,
  '$' || to_char(sum(total), 'FM999,999,999,999.99') as "Subtotal"
from
  invoice
where
  issued_at > '2022-03-01'
  and updated_at > '2022-03-31'
group by
  plan_id,
  plan_name,
  status;

-- This is once again one that may have been deceptive in its simplicity?
-- Based on the one line requirement and 30 second talk we had, I queried on the invoices and grouped by the
-- current plan name.
-- The dates are hardcoded and would of course be argument sin production.