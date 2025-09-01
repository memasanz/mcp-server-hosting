# MCP Weather Server (uv-managed)

This is an MCP (Model Context Protocol) weather server that provides weather alerts and forecasts using the National Weather Service API. It uses FastMCP with streamable HTTP transport and is deployed on Azure Container Apps.

## MCP Tools
- `get_alerts(state)` -> Get weather alerts for a US state (e.g., "MN", "CA")
- `get_forecast(latitude, longitude)` -> Get weather forecast for specific coordinates

## Server Endpoint
- **MCP Endpoint**: `/mcp` - Main MCP protocol endpoint for tool calls
- **Health Check**: `/api/health` - Health status endpoint for monitoring and Azure Container Apps probes

## Local Development Setup

### Prerequisites
Install `uv` if you don't have it:

```powershell
# Windows PowerShell
pip install uv
```

### After Cloning the Repository

1. Navigate to the python directory:
```powershell
cd python
```

2. Create a virtual environment and install dependencies:
```powershell
uv venv
uv sync
```

This will:
- Create a `.venv` folder with the Python virtual environment
- Install all dependencies specified in `pyproject.toml` and `uv.lock`
- Set up the environment exactly as specified in the lock file

### Running the Server Locally

Run the MCP server using uvicorn:

```powershell
# Windows PowerShell
.venv\Scripts\uvicorn.exe app.main:app --reload --host 127.0.0.1 --port 8000
```

The MCP server will be available at:
- **MCP Endpoint**: `http://127.0.0.1:8000/mcp`

### Testing with MCP Inspector

1. Install and run MCP Inspector:
```powershell
npx @modelcontextprotocol/inspector
```

2. In the MCP Inspector UI, connect using:
- **Transport**: Streamable HTTP
- **URL**: `http://127.0.0.1:8000/mcp`

3. Test the weather tools:
- Try `get_alerts` with state "MN" 
- Try `get_forecast` with coordinates like 44.9778, -93.2650 (Minneapolis)

## Docker

Build and run locally:

```powershell
# From the python/ folder
docker build -t mcp-weather-server .
docker run --rm -p 8000:8000 mcp-weather-server
```

The containerized server will be available at `http://localhost:8000/mcp`

## Azure Container Apps Deployment

This server is deployed to Azure Container Apps using Azure Container Registry (ACR) build approach to bypass Oryx build system issues.

### Prerequisites
- Azure CLI installed and logged in
- Azure Container Registry (ACR) 
- Azure Container Apps environment

### Build and Deploy Commands

1. **Build the image using ACR** (from the `python/` directory):
```powershell
# Build and push to ACR in one step
az acr build --registry <your-registry-name> --image mcp-weather-server:latest .
```

2. **Create or update the Container App**:
```powershell
# Create container app (first time)
az containerapp create \
  --name weather-mcp-http-v2 \
  --resource-group <your-resource-group> \
  --environment <your-environment-name> \
  --image <your-registry-name>.azurecr.io/mcp-weather-server:latest \
  --target-port 8000 \
  --ingress external \
  --registry-server <your-registry-name>.azurecr.io

# Or update existing container app
az containerapp update \
  --name weather-mcp-http-v2 \
  --resource-group <your-resource-group> \
  --image <your-registry-name>.azurecr.io/mcp-weather-server:latest
```

3. **Complete deployment workflow**:
```powershell
# From the python/ directory
# 1. Build and push
az acr build --registry <your-registry-name> --image mcp-weather-server:latest .

# 2. Update container app with new image
az containerapp update \
  --name weather-mcp-http-v2 \
  --resource-group <your-resource-group> \
  --image <your-registry-name>.azurecr.io/mcp-weather-server:latest

# 3. Get the app URL
az containerapp show \
  --name weather-mcp-http-v2 \
  --resource-group <your-resource-group> \
  --query "properties.configuration.ingress.fqdn" \
  --output tsv
```

### Deployed Endpoint
After deployment, your MCP server will be available at:
- **MCP Endpoint**: `https://<your-app-name>.<region>.azurecontainerapps.io/mcp`

### Why ACR Build?
We use `az acr build` instead of local Docker builds because:
- Bypasses Azure Container Apps Oryx build system interference 
- Builds directly in Azure with optimized caching
- Automatically pushes to the registry
- Works better with uv-based Python projects

## Dependencies & Architecture

- **FastMCP**: Framework for building MCP servers with streamable HTTP transport
- **httpx**: HTTP client for calling National Weather Service API
- **uvicorn**: ASGI server for running the FastAPI application
- **uv**: Fast Python package manager for dependency management

## Notes
- `uv` manages dependencies and virtual environments
- Server uses FastMCP's streamable HTTP transport for MCP protocol communication
- Weather data comes from the National Weather Service API (no API key required)
- Requires Python 3.12+ (as specified in Dockerfile)
- `.venv` folder is git-ignored - run `uv sync` after cloning