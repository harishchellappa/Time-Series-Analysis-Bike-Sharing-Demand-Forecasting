Create table market1
(
	Item_Group_Product_Family	varchar(50),
Item_no	varchar(50),
Year_Month_order_date	varchar(50),
Total	integer
);

select distinct Year_Month_order_date 
			from market1																		
into #dummy;

create temp table 	temp1 as
select distinct Year_Month_order_date 
from market1

select count(*)
from market1

select distinct a.Item_Group_Product_Family, a.Item_no
into first2columns
from market1 a

select a.*, b.*
into first3columns
from first2columns a
cross join temp1 b

select a.*, coalesce (b.Total,0)
into first4columns
from first3columns a
left outer join market1 b
on a.Item_Group_Product_Family = b.Item_Group_Product_Family
and a.Item_no = b.Item_no
and a.Year_Month_order_date = b.Year_Month_order_date




select count(*)
from markettest1

select distinct *
into markettest2
from markettest1

select b.Item_Group_Product_Family,b.Item_no,b.Year_Month_order_date
into markettest3
from market1 a
inner join markettest2 b
on a.Item_Group_Product_Family = b.Item_Group_Product_Family
and a.Item_no = b.Item_no
--and b.Year_Month_order_date = a.Year_Month_order_date

select count(*)
from market1

cross join temp1 b
		( select b.Year_Month_order_date 
			from market1 b																		
)t1;