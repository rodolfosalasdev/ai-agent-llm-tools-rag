from ai_agent.agent import graph


def test_run_agent_uses_langgraph_invoke(mocker):
    mock_agent = mocker.Mock()
    mock_agent.invoke.return_value = {
        "messages": [mocker.Mock(content="Resposta mockada do agente")]
    }
    mocker.patch("ai_agent.agent.graph.build_agent", return_value=mock_agent)

    answer = graph.run_agent("Qual o prazo de devolução?")

    assert answer == "Resposta mockada do agente"
    mock_agent.invoke.assert_called_once()
