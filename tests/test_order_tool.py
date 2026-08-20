from ai_agent.tools.order_tool import get_order_status


def test_get_order_status_known_order():
    result = get_order_status.invoke({"order_id": "ord-12345"})
    assert "ORD-12345" in result
    assert "shipped" in result


def test_get_order_status_unknown_order():
    result = get_order_status.invoke({"order_id": "ORD-99999"})
    assert "não encontrado" in result.lower()
