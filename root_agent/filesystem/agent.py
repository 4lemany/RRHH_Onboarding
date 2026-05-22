"""ADK agent with MCP tools from a local notes MCP server."""

import os

from google.adk import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams

try:
    from tutorials.model_config import get_model
except ModuleNotFoundError:
    from pathlib import Path
    import sys

    tutorials_dir = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(tutorials_dir))
    from model_config import get_model

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:9001/sse")

root_agent = Agent(
    model=get_model(),
    name="root_agent",
    description="Es el agente orquestador que decide que hacer.",
    instruction=(
        "Si el usuario hace preguntas sobre impuestos, facturación, IVA o cuentas, usa la herramienta consultar_contabilidad. Si hace preguntas sobre contratos, despidos o nóminas, usa consultar_laboral. Si es un saludo o pregunta fuera de tema, responde tú mismo de forma sencilla."
    ),
    tools=[
        McpToolset(
            connection_params=SseConnectionParams(
                url=MCP_SERVER_URL,
                timeout=30,
            ),
            tool_filter=["create_note", "list_notes", "read_note"],
        ),
    ],
)
