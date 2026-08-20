from pathlib import Path

from ai_agent.rag.vectorstore import load_markdown_documents


def test_load_markdown_documents():
    knowledge_dir = Path(__file__).resolve().parents[1] / "data" / "knowledge"
    docs = load_markdown_documents(knowledge_dir)

    assert len(docs) >= 2
    assert any("FAQ" in doc.page_content for doc in docs)
    assert all("source" in doc.metadata for doc in docs)
