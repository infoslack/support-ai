from sqlalchemy import create_engine, text
from config.settings import settings

engine = create_engine(settings.database_url)


def get_order_data(order_id: str, customer_id: str) -> dict | None:
    query = text("""
        SELECT
            o.id AS order_id,
            o.status,
            o.total_value,
            o.created_at,
            o.delivered_at,
            o.estimated_delivery_at,
            r.name AS restaurant_name,
            r.is_open AS restaurant_is_open,
            c.name AS customer_name,
            c.total_orders AS customer_total_orders,
            c.refunds_last_30_days,
            (
                SELECT COUNT(*) FROM orders o2
                WHERE o2.customer_id = o.customer_id
                AND o2.created_at >= NOW() - INTERVAL '30 days'
            ) AS recent_orders
        FROM orders o
        JOIN restaurants r ON o.restaurant_id = r.id
        JOIN customers c ON o.customer_id = c.id
        WHERE o.id = :order_id AND o.customer_id = :customer_id
    """)

    with engine.connect() as conn:
        row = conn.execute(
            query, {"order_id": order_id, "customer_id": customer_id}
        ).fetchone()
        if not row:
            return None
        return dict(row._mapping)


def format_order_context(data: dict) -> str:
    delivered = data.get("delivered_at")
    estimated = data.get("estimated_delivery_at")

    late_minutes = None
    if delivered and estimated:
        delta = delivered - estimated
        late_minutes = int(delta.total_seconds() / 60)

    lines = [
        f"Order ID: {data['order_id']}",
        f"Status: {data['status']}",
        f"Total value: R${data['total_value']:.2f}",
        f"Restaurant: {data['restaurant_name']} ({'open' if data['restaurant_is_open'] else 'closed'})",
        f"Customer: {data['customer_name']}",
        f"Customer total orders: {data['customer_total_orders']}",
        f"Refunds in last 30 days: {data['refunds_last_30_days']}",
        f"Order placed at: {data['created_at']}",
    ]

    if late_minutes is not None:
        if late_minutes > 0:
            lines.append(f"Delivery was {late_minutes} minutes late")
        else:
            lines.append("Delivery was on time")

    if not delivered:
        lines.append("Order has NOT been delivered yet")

    return "\n".join(lines)
