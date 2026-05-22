from google.adk import Agent

from tutorials.model_config import get_model

# =============================================================
# Agent: consulta_laboral (Uses MCP notes server)
# =============================================================

from google.adk import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams

# MCP server URL for laboral topics (e.g., a different server than contabilidad)
LABORAL_MCP_URL = os.getenv("LABORAL_MCP_URL", "http://127.0.0.1:9002/sse")

consultar_laboral = Agent(
    model=get_model(),
    name="consultar_laboral",
    description="Asesoría en temas laborales (contratos, despidos, nóminas, seguridad social).",
    instruction=(
        """Eres un asesor laboral. Usa las herramientas MCP disponibles para responder preguntas sobre:
        contratos de trabajo (tipos, duración, modificaciones)
        despidos (causas, indemnizaciones, procedimientos)
        nóminas y conceptos salariales
        seguridad social, autónomos, cotizaciones
        vacaciones y permisos
        Eres conciso y claro."""
    ),

    tools=[
        McpToolset(
            connection_params=SseConnectionParams(
                url=LABORAL_MCP_URL,
                timeout=30,
            ),
            # You can filter tools from the laboral server as needed,
            # e.g., specific files or tool names.
            tool_filter=["contratos.txt", "despidos.txt", "nominas.txt"],
        )
    ],
)


roll_die_agent = Agent(
    model=get_model(),
    name="roll_die_agent",
    description=(
        "Rolls dice. Input: how many rolls and how many sides (default 6). "
        "Output: comma-separated results, e.g. 'Results: 3, 5, 1, 6, 2'."
    ),
    instruction=(
        "You are a dice-rolling assistant. You can ONLY roll dice using the roll_die tool.\n"
        "When asked to roll a die N times, call roll_die once for EACH roll requested.\n"
        "Always reply with the results as a comma-separated list, e.g.: 'Results: 3, 5, 1, 6, 2'.\n"
        "If the user does not specify the number of sides, assume 6.\n"
        "Do NOT make up results. Always call the roll_die tool."
    ),
    tools=[roll_die],
)
