-- Q004 (Lower) Reference Solution: Late Delivery List
-- Expected output (sample, first 5 rows):
-- shipment_id, carrier, promised_date, first_delivered_date, days_late
-- shipment_00339, postal_economy, 2024-07-04, 2024-07-08, 4
-- shipment_00393, postal_economy, 2024-07-17, 2024-07-21, 4
-- shipment_00050, postal_economy, 2024-05-19, 2024-05-22, 3
-- shipment_00156, postal_economy, 2024-07-31, 2024-08-03, 3
-- shipment_00162, postal_economy, 2024-07-12, 2024-07-15, 3

with delivered_event_dates as (
    select
        shipment_events.shipment_id,
        min(shipment_events.event_date) as first_delivered_date
    from shipment_events
    where shipment_events.event_type = 'delivered'
    group by
        shipment_events.shipment_id
),
shipment_exception_candidates as (
    select
        shipments.shipment_id,
        shipments.carrier,
        shipments.promised_date,
        delivered_event_dates.first_delivered_date
    from shipments
    left join delivered_event_dates
        on shipments.shipment_id = delivered_event_dates.shipment_id
)
select
    shipment_exception_candidates.shipment_id,
    shipment_exception_candidates.carrier,
    shipment_exception_candidates.promised_date,
    shipment_exception_candidates.first_delivered_date,
    shipment_exception_candidates.first_delivered_date - shipment_exception_candidates.promised_date as days_late
from shipment_exception_candidates
where shipment_exception_candidates.first_delivered_date > shipment_exception_candidates.promised_date
order by
    days_late desc,
    shipment_exception_candidates.shipment_id;
