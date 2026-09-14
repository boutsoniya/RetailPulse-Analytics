# RetailPulse Data Dictionary

The primary dataset is a synthetic retail transaction table. It is generated reproducibly and is intended for academic/portfolio demonstration only.

## Grain

One row represents one retail order line / transaction.

| Field | Type | Description |
|---|---|---|
| order_id | text | Unique transaction/order identifier |
| order_date | date | Date on which the order was recorded |
| customer_id | text | Customer identifier |
| customer_name | text | Synthetic customer label |
| gender | category | Synthetic customer gender category |
| age | integer | Customer age at transaction time |
| city | text | Customer city |
| state | text | Customer state |
| region | category | North, South, East or West |
| channel | category | Store, Website or Mobile App |
| product_id | text | Product identifier |
| product_name | text | Product name |
| category | category | Product category |
| subcategory | category | Product subcategory |
| quantity | integer | Units purchased in the transaction |
| unit_price | numeric | List price per unit in INR |
| discount_pct | numeric | Discount percentage applied |
| revenue | numeric | Net transaction revenue in INR |
| unit_cost | numeric | Cost per unit in INR |
| cost | numeric | Total estimated cost in INR |
| profit | numeric | Revenue minus estimated cost in INR |
| payment_method | category | Payment method used |

## Derived analytical measures

- **Revenue** = quantity × unit_price × (1 − discount_pct)
- **Cost** = quantity × unit_cost
- **Profit** = revenue − cost
- **Profit Margin %** = profit / revenue × 100
- **Average Order Value** = revenue / distinct orders
- **Recency** = days since the customer's latest order relative to the analysis snapshot date.
- **Frequency** = number of distinct orders for a customer.
- **Monetary** = total revenue attributed to a customer.

## Data governance note

Names and transaction records are synthetic. No real customer PII or confidential company records are included.
