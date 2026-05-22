```mermaid
graph TD
    Usuario[Usuario] -->|Consulta| Orquestador[Agente Orquestador (Cliente MCP)]
    Orquestador -->|Filtro / Saludo / Off-topic| Usuario
    Orquestador -->|Consulta Especializada| ServidorMCP[Servidor MCP Asesoría]
    ServidorMCP -->|Herramienta: consultar_contabilidad| AgenteContable[Agente Contable (Especialista)]
    ServidorMCP -->|Herramienta: consultar_laboral| AgenteLaboral[Agente Laboral (Especialista)]
```
