# AI Agent — LLM + Tools + RAG

Exemplo profissional de agente de suporte em **Python** usando **LangGraph**, **LangChain**, **OpenAI** e **ChromaDB**.

Este repositório complementa o [agent-service](https://github.com/rodolfosalasdev/agent-service): enquanto o NestJS mostra como **expor** um agente via API, aqui focamos no **cérebro** do agente — RAG, tools e orquestração ReAct.

## O que este projeto faz

- Indexa documentos Markdown locais (`data/knowledge/`) em um vector store **ChromaDB**
- Expõe a tool `search_support_knowledge` para busca semântica (RAG)
- Expõe a tool `get_order_status` para consulta de pedidos demo
- Orquestra tudo com **LangGraph** (`create_react_agent`) — padrão ReAct moderno
- CLI `ai-agent ask "pergunta"` para testar interativamente

## Por que Python + LangGraph + Chroma?

| Tecnologia | Motivo |
|---|---|
| **Python** | Ecossistema mais maduro para LLM, RAG e prototipagem rápida |
| **LangGraph** | Grafo de agente explícito, estado tipado, padrão ReAct de mercado |
| **LangChain** | Pipeline de documentos, splitters, embeddings e integrações |
| **ChromaDB** | Vector store local, zero infra extra, ideal para estudo |
| **OpenAI** | Embeddings + chat com qualidade consistente |
| **Typer + Rich** | CLI profissional para demos e testes manuais |

Escolhemos **Chroma local** em vez de Pinecone/Weaviate para manter o exemplo autocontido. Em produção, você trocaria apenas a camada de vector store.

## Arquitetura

```text
User Question
     │
     ▼
LangGraph ReAct Agent
     ├── tool: search_support_knowledge ──► Chroma retriever ──► FAQ/Policies
     └── tool: get_order_status ──► catálogo demo de pedidos
     │
     ▼
Final Answer
```

## Pré-requisitos

- Python 3.11+
- Chave OpenAI (`OPENAI_API_KEY`)

## Como rodar

```bash
git clone https://github.com/rodolfosalasdev/ai-agent-llm-tools-rag.git
cd ai-agent-llm-tools-rag
git checkout develop

python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

cp .env.example .env
# Edite .env com sua OPENAI_API_KEY
```

### Perguntas de exemplo

```bash
# RAG sobre política
ai-agent ask "Qual o prazo para solicitar devolução?"

# Tool de pedido
ai-agent ask "Qual o status do pedido ORD-12345?"

# Combina contexto + pedido
ai-agent ask "Tenho o pedido ORD-67890, quanto tempo falta?"
```

Pedidos demo: `ORD-12345`, `ORD-67890`, `ORD-00001`.

## Testes

```bash
pytest
```

Testes mockam o grafo LangGraph — não consomem créditos OpenAI.

## Estrutura

```text
src/ai_agent/
  agent/graph.py       # LangGraph ReAct agent
  rag/vectorstore.py   # ingest + retriever tool
  tools/order_tool.py  # tool de pedidos
  cli.py               # Typer CLI
data/knowledge/        # documentos indexados
tests/
```

## Limitações intencionais (demo)

- Vector store local (`.chroma/`) — recriado na primeira execução
- Documentos estáticos em Markdown
- Sem API HTTP (virá no projeto orquestrador com frontend)

## Repositórios relacionados

- [agent-service](https://github.com/rodolfosalasdev/agent-service) — NestJS + tool calling HTTP
- [multi-agents-crewai](https://github.com/rodolfosalasdev/multi-agents-crewai) — multi-agente com CrewAI

## Licença

MIT
