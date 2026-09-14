# RetailPulse Data Dictionary

## Grain

One row represents one retail order line / transaction.

| Column | Type | Description |
|---|---|---|
| order_id | string | Unique order identifier |
| order_date | date | Date on which the order was placed |
| customer_id | string | Unique customer identifier |
| customer_name | string | Synthetic customer name |
| gender | category | Customer gender used for descriptive analysis |
| age | integer | Customer age |
| city | string | Customer city |
| state | string | Customer state |
| region | category | North, South, East or West |
| channel | category | Store, Website or Mobile App |
| product_id | string | Unique product identifier |
| product_name | string | Product name |
| category | category | Product category |
| subcategory | category | Product subcategory |
| quantity | integer | Units purchased |
| unit_price | float | Selling price per unit before discount |
| discount_pct | float | Discount percentage applied |
| revenue | float | Net sales value after discount |
| unit_cost | float | Cost per unit |
| cost | float | Total product cost |
| profit | float | Revenue minus cost |
| payment_method | category | Payment method |

## Derived metrics

- **Revenue** = quantity × unit_price × (1 − discount_pct)
- **Cost** = quantity × unit_cost
- **Profit** = revenue − cost
- **Profit Margin %** = profit / revenue × 100
- **Average Order Value** = revenue / distinct orders

All records are synthetic and generated for this project.
