# REST API design

Planned HTTP API for `orders-service` (stage 3, FastAPI). It mirrors what the CLI can do today.
Every order gets an integer `id` assigned by the server. Request and response bodies are JSON
(`Content-Type: application/json`), except the CSV export.

## Endpoints

| Action | Method | Path | Request body | Success | Errors |
|---|---|---|---|---|---|
| List orders | GET | `/orders?status=&urgent=&overdue=` | — | `200`, list of orders (`[]` if none match) | `422` unknown `status` value |
| Get one order | GET | `/orders/{id}` | — | `200`, the order | `404` no order with this `id` |
| Create order | POST | `/orders` | order fields | `201`, created order + `Location` header | `422` invalid data (e.g. `pages` ≤ 0, unknown `work_type`, deadline in the past) |
| Change status | PATCH | `/orders/{id}` | `{"status": "done"}` | `200`, updated order | `404` no order with this `id`; `422` unknown status |
| Delete order | DELETE | `/orders/{id}` | — | `204`, no body | `404` no order with this `id` |
| Statistics | GET | `/orders/stats` | — | `200`, stats object | — |
| Export to CSV | GET | `/orders/export?status=` | — | `200`, CSV file (`Content-Type: text/csv`) | `422` unknown `status` value |

All filters are optional and combine with AND: `/orders?status=new&urgent=true` returns urgent new orders.

## Example: create an order

Request. The client does not send `id`, `status` or `price`: the server sets them.

```http
POST /orders HTTP/1.1
Content-Type: application/json

{
  "customer": "Антон",
  "work_type": "homework",
  "pages": 20,
  "deadline": "2027-03-15",
  "rate": 30,
  "urgent": false
}
```

Response:

```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /orders/7

{
  "id": 7,
  "customer": "Антон",
  "work_type": "homework",
  "pages": 20,
  "deadline": "2027-03-15",
  "rate": 30,
  "status": "new",
  "urgent": false,
  "price": 600
}
```

Response to invalid data (`"pages": 0`):

```http
HTTP/1.1 422 Unprocessable Content
Content-Type: application/json

{"detail": "pages: must be greater than 0"}
```

## Example: statistics

```http
GET /orders/stats HTTP/1.1
```

```json
{
  "total_orders": 12,
  "total_revenue": 9400,
  "urgent_count": 3,
  "by_type": {"notes": 5, "homework": 6, "report": 1}
}
```
