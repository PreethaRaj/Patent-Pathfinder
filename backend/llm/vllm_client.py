import httpx

from backend.llm.base import LLMProvider

class VLLMClient(LLMProvider):
    def __init__(self, base_url: str, chat_model: str, embedding_model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.chat_model = chat_model
        self.embedding_model = embedding_model

    async def chat(self, messages: list, tools: list) -> dict:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": self.chat_model,
                    "messages": messages,
                    "tools": tools,
                    "tool_choice": "auto" if tools else "none",
                    "temperature": 0.2,
                },
            )
            response.raise_for_status()
            return response.json()

    async def embed(self, texts: list[str]) -> list[list[float]]:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/v1/embeddings",
                json={"model": self.embedding_model, "input": texts},
            )
            response.raise_for_status()
            payload = response.json()
            return [item["embedding"] for item in payload["data"]]

    async def tool_call(self, tool_name: str, **kwargs) -> dict:
        return {"tool_name": tool_name, "provider": "vllm", "arguments": kwargs}
