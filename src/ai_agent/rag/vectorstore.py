from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings

from ai_agent.config import settings


def load_markdown_documents(knowledge_dir: str | Path) -> list[Document]:
    root = Path(knowledge_dir)
    documents: list[Document] = []

    for file_path in sorted(root.glob("**/*.md")):
        content = file_path.read_text(encoding="utf-8")
        documents.append(
            Document(
                page_content=content,
                metadata={"source": str(file_path.relative_to(root))},
            )
        )

    return documents


def build_vector_store(
    knowledge_dir: str | Path | None = None,
    persist_dir: str | None = None,
) -> Chroma:
    docs = load_markdown_documents(knowledge_dir or settings.knowledge_dir)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    chunks = splitter.split_documents(docs)

    return Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(
            model=settings.openai_embedding_model,
            api_key=settings.openai_api_key,
        ),
        persist_directory=persist_dir or settings.chroma_persist_dir,
        collection_name="support-knowledge",
    )


def create_knowledge_search_tool(vector_store: Chroma):
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    @tool
    def search_support_knowledge(query: str) -> str:
        """Search internal FAQ/policy documents to answer product and policy questions."""

        docs = retriever.invoke(query)
        if not docs:
            return "Nenhum documento relevante encontrado."

        formatted = []
        for index, doc in enumerate(docs, start=1):
            source = doc.metadata.get("source", "unknown")
            formatted.append(f"[{index}] ({source})\n{doc.page_content}")

        return "\n\n".join(formatted)

    return search_support_knowledge
