"""Local agent: computes distribution statistics (mean and standard deviation)."""


from google.adk import Agent

from tutorials.model_config import get_model

# =============================================================
# Agent: consulta_laboral (Uses MCP notes server)
# =============================================================

from google.adk import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams

# MCP server URL for laboral topics (e.g., a different server than contabilidad)
FINANCIAL_MCP_URL = os.getenv("FINANCIAL_MCP_URL", "http://127.0.0.1:9003/sse")

financial_agent = Agent(
    model=get_model(),
    name="financial_agent",
    description="Asesoría en temas financieros y contables.",
    instruction=(
        """Eres un asesor financiero y contable. Usa las herramientas MCP disponibles para responder preguntas sobre:
        facturas y presupuestos
        impuestos y tasas
        cuentas y balances
        costos y gastos
        cuentas anuales
        ERES CONCISO Y CLARO."""
    ),
    tools=[
        McpToolset(
            connection_params=SseConnectionParams(
                url=FINANCIAL_MCP_URL,
                timeout=30,
            ),
            tool_filter=["facturas.txt", "impuestos.txt", "cuentas.txt"],
        )
    ],
)
