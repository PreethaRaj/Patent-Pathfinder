import httpx

class MCPClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    async def command(self, command: str, arguments: dict) -> dict:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/mcp/command",
                json={"command": command, "arguments": arguments},
            )
            response.raise_for_status()
            return response.json()
