# agents-tutorials

Hands-on tutorials and examples for building agents with the
[Google ADK](https://google.github.io/adk-docs/), MCP, A2A, evaluations
and Vertex AI.

## Table of contents

- [Prerequisites](#prerequisites)
  - [Install uv](#install-uv)
  - [Install the Google Cloud SDK (`gcloud`)](#install-the-google-cloud-sdk-gcloud)
  - [Install dependencies](#install-dependencies)
- [Repository layout](#repository-layout)
- [Configuration](#configuration)
  - [Model provider options](#model-provider-options)
- [Tutorials](#tutorials)
- [Notebooks](#notebooks)
- [Development](#development)

---

## Prerequisites

This project targets **Python 3.12** (see `.python-version`).

### Install uv

[`uv`](https://docs.astral.sh/uv/) is the Python package & project manager
used in this repository.

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installing, restart your terminal so the `uv` command is available.

Reference: [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/).

### Install the Google Cloud SDK (`gcloud`)

The `gcloud` CLI is required for the Vertex AI model provider, the GCP
deployment tutorial (`t08_deploy_gcp`), the local RAG tutorial
(`t09_local_rag_agent`) and the Vertex AI Search tutorial
(`t10_vertex_search_agent`).

Official installation guide: <https://cloud.google.com/sdk/docs/install>

**macOS** (recommended via Homebrew):

```bash
brew install --cask google-cloud-sdk
```

Or follow the manual installer: <https://cloud.google.com/sdk/docs/install#mac>

**Linux:**

```bash
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/install_google_cloud_sdk.bash
bash install_google_cloud_sdk.bash
```

Or follow: <https://cloud.google.com/sdk/docs/install#linux>

**Windows:**

Download and run the installer from
<https://cloud.google.com/sdk/docs/install#windows>.

#### Initialise and authenticate

After installing, restart your terminal and run:

```bash
gcloud init
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

`gcloud auth application-default login` writes credentials to
`~/.config/gcloud/application_default_credentials.json`, which the
Google Gen AI SDK and Vertex AI client libraries pick up automatically —
no API key needed.

Enable the APIs used in the tutorials:

```bash
gcloud services enable \
  aiplatform.googleapis.com \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  storage.googleapis.com \
  discoveryengine.googleapis.com
```

Useful references:

- [Initialising the gcloud CLI](https://cloud.google.com/sdk/docs/initializing)
- [Authorising the gcloud CLI](https://cloud.google.com/sdk/docs/authorizing)
- [Application Default Credentials (ADC)](https://cloud.google.com/docs/authentication/provide-credentials-adc)
- [Vertex AI documentation](https://cloud.google.com/vertex-ai/docs)
- [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/docs/agent-engine/overview)
- [Cloud Run documentation](https://cloud.google.com/run/docs)
- [Vertex AI Search documentation](https://cloud.google.com/generative-ai-app-builder/docs/introduction)

### Install dependencies

Install the core project + dev dependencies:

```bash
uv sync
```

Install the ADK tutorials (most tutorials need this):

```bash
uv sync --extra adk
```

Other extras can be combined with `--extra`:

| Extra        | Used by                                                  |
| ------------ | -------------------------------------------------------- |
| `adk`        | All ADK-based tutorials (`t01`–`t06`, `t08`–`t10`)       |
| `notebooks`  | Jupyter notebooks under `notebooks/`                     |
| `eval`       | Tutorial 7 — DeepEval evaluations                        |
| `rag`        | Tutorial 9 — Local FAISS RAG agent                       |
| `dev`        | `pytest` + `ruff` for local development                  |

Common combinations:

```bash
# ADK tutorials + notebooks
uv sync --extra adk --extra notebooks

# Evaluations
uv sync --extra adk --extra eval

# Local RAG (tutorial 9)
uv sync --extra adk --extra notebooks --extra rag
```

Quick sanity check:

```bash
uv run python -c "from agents_tutorials import __version__; print(__version__)"
```

---

## Repository layout

```text
.
├── notebooks/              # Jupyter notebooks (RAG indexing, GCP clients, evals…)
├── src/
│   ├── agents_tutorials/   # Shared package
│   └── tutorials/          # Step-by-step tutorials (ADK, MCP, A2A, evals, GCP)
├── tests/                  # Pytest test suite
├── Makefile                # lint / format / test shortcuts
├── pyproject.toml          # uv project definition with extras
├── .env.example            # Template for environment variables
└── uv.lock
```

---

## Configuration

All tutorials read the same environment variables. Copy the template and
edit it to your needs:

```bash
cp .env.example .env
```

Load it into the current bash shell with:

```bash
set -a && source .env && set +a
```

### Model provider options

Tutorials support three LLM backends, selected with `MODEL_PROVIDER`.

#### Option A: Gemini (default)

```bash
export MODEL_PROVIDER=gemini
export GOOGLE_API_KEY="your-gemini-api-key"
```

Get an API key at <https://aistudio.google.com/app/apikey>.

#### Option B: Groq

```bash
export MODEL_PROVIDER=groq
export GROQ_API_KEY="your-groq-api-key"
```

Get an API key at <https://console.groq.com/keys>.

#### Option C: Vertex AI

One-time auth on your machine (requires `gcloud` — see
[Install the Google Cloud SDK](#install-the-google-cloud-sdk-gcloud)):

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

Then configure Vertex:

```bash
export MODEL_PROVIDER=vertex
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
export GOOGLE_CLOUD_LOCATION="global"
# optional
export VERTEX_MODEL="gemini-2.5-flash-lite"
```

See [`.env.example`](.env.example) for the full list of variables, including
those used by the GCP deployment, MCP, local RAG and Vertex AI Search
tutorials.

---

## Tutorials

### 1. Tutorial Agent

A minimal starter agent with one mock time tool. See `src/tutorials/t01_tutorial_agent/README.md`.

### 2. Basic ADK Agent

A single agent with one Python function tool (dice rolling). See `src/tutorials/t02_basic_agent/README.md`.

### 3. Sequential Workflow Agent

A deterministic pipeline using `SequentialAgent`: two sub-agents run in a fixed order defined in code (researcher then summarizer), not decided by an LLM. See `src/tutorials/t03_sequential_agent/README.md`.

### 4. Multi-Agent (Local)

A supervisor agent orchestrating two local sub-agents (dice roller + stats calculator) using `AgentTool`. See `src/tutorials/t04_multi_agent/README.md`.

### 5. ADK Agent with MCP Tool

A step-by-step MCP tutorial: run a separate notes MCP server and connect to it from both a standalone client and an ADK agent. See `src/tutorials/t05_mcp_agent/README.md`.

### 6. Remote A2A Agents

Three remote agents communicating via the A2A protocol, each with its own agent card and HTTP server. See `src/tutorials/t06_remote_a2a/README.md`.

### 7. Agent Evaluations with DeepEval

Evaluate the multi-agent supervisor with a golden dataset and DeepEval metrics. See `src/tutorials/t07_evaluations/README.md`.

Install eval dependencies and run:

```bash
uv sync --extra adk --extra eval
uv run pytest src/tutorials/t07_evaluations/ -v
```

### 8. Deploy ADK Agent to GCP

Deploy a self-contained dice agent to Cloud Run and Vertex AI Agent Engine using `adk deploy`. Requires `gcloud`. See `src/tutorials/t08_deploy_gcp/README.md`.

### 9. Local RAG Agent

Download a PDF, build a local FAISS index in a notebook, then query it from an ADK agent using `LlamaIndexRetrieval`. See `src/tutorials/t09_local_rag_agent/README.md`.

### 10. Vertex AI Search Agent

Download a PDF, import it into a Vertex AI Search data store, then query it from an ADK agent using `VertexAiSearchTool` (model-native Gemini grounding). Requires `gcloud`. See `src/tutorials/t10_vertex_search_agent/README.md`.

---

## Notebooks

Install notebook dependencies and start Jupyter:

```bash
uv sync --extra adk --extra notebooks
uv run jupyter notebook notebooks/
```

For the local RAG notebook, install the RAG extra too:

```bash
uv sync --extra adk --extra notebooks --extra rag
```

- `notebooks/deploy_gcp_clients.ipynb` — call the deployed GCP agent from Cloud Run and Agent Engine.
- `notebooks/evaluations.ipynb` — interactive companion for tutorial 7.
- `notebooks/mcp_tool_discovery.ipynb` — discover and invoke tools from an MCP server.
- `notebooks/local_rag_indexing.ipynb` — download a PDF, create chunks, build the local FAISS index and test retrieval for tutorial 9.
- `notebooks/vertex_search_indexing.ipynb` — download a PDF, upload it to GCS and import it into a Vertex AI Search data store for tutorial 10.

---

## Development

The `Makefile` provides shortcuts for the most common tasks:

```bash
make lint         # ruff check
make lint-fix     # ruff check --fix
make format       # ruff format
make format-check # ruff format --check
make fix          # lint-fix + format
make check        # lint + format-check
make test         # pytest
```
#   a s e s o r - c o n t a b l e - l a b o r a l  
 