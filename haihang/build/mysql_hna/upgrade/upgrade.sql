use caas_payment;


alter table bill_bill add column name varchar(50) default '';
alter table bill_billrecord add column name varchar(50);

alter table price_price change effective_date effective_date date;