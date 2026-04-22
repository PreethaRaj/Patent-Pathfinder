from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

class MCPCommand(BaseModel):
    command: str
    arguments: dict[str, Any] = Field(default_factory=dict)

def create_mcp_app(name: str, version: str, handlers: dict[str, Callable[[dict[str, Any]], Awaitable[dict]]]) -> FastAPI:
    app = FastAPI(title=name, version=version)

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/mcp")
    async def info() -> dict[str, Any]:
        return {
            "server": name,
            "version": version,
            "protocol": "model-context-protocol",
            "commands": sorted(handlers.keys()),
        }

    @app.post("/mcp/command")
    async def execute(payload: MCPCommand) -> dict:
        handler = handlers.get(payload.command)
        if not handler:
            raise HTTPException(status_code=404, detail=f"Unknown command: {payload.command}")
        return await handler(payload.arguments)

    return app
