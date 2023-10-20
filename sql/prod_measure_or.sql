select
prod_id, prod_name, prod_measure, prod_price
from products
where
prod_measure = '$prod_measure1'
OR
prod_measure = '$prod_measure2'