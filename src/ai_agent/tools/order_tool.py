from langchain_core.tools import tool


@tool
def get_order_status(order_id: str) -> str:
    """Return shipping status for a demo order id such as ORD-12345."""

    catalog = {
        "ORD-12345": {"status": "shipped", "eta_days": 2, "carrier": "Correios"},
        "ORD-67890": {"status": "processing", "eta_days": 5, "carrier": "Loggi"},
        "ORD-00001": {"status": "delivered", "eta_days": 0, "carrier": "Correios"},
    }

    normalized = order_id.strip().upper()
    order = catalog.get(normalized)
    if not order:
        return f"Pedido {normalized} não encontrado no catálogo demo."

    return (
        f"Pedido {normalized}: status={order['status']}, "
        f"transportadora={order['carrier']}, eta_days={order['eta_days']}"
    )
