# Q004 (Lower) - Late Delivery List

**Level:** Lower (entry to early-career analytics engineering)  
**Concepts tested:** left joins, first-event logic, date comparison filters

---

## Scenario

You are helping operations review late deliveries.

You have two tables:

### `shipments`
| column | type | description |
|--------|------|-------------|
| `shipment_id` | varchar | unique shipment identifier |
| `ship_date` | date | date shipment left the warehouse |
| `carrier` | varchar | shipping carrier (`parcel_fast`, `regional_ground`, `postal_economy`) |
| `promised_date` | date | date promised to the customer |

### `shipment_events`
| column | type | description |
|--------|------|-------------|
| `shipment_id` | varchar | shipment identifier |
| `event_date` | date | date event occurred |
| `event_type` | varchar | event type (`delivered`, `exception`) |

---

## Question

Return one row per shipment that was delivered late:

- `shipment_id`
- `carrier`
- `promised_date`
- `first_delivered_date` (first `delivered` event per shipment)
- `days_late` (`first_delivered_date - promised_date`)

Include only shipments where `first_delivered_date > promised_date`.

Order by `days_late` descending, then `shipment_id`.

---

## Data

Connect to: `data/duckdb/workspace_verify.duckdb` and run `USE workspace_db.q004_lower;` (see `scratchpad.sql`).
