# mcp-server-hub

Collection of MCP (Model Context Protocol) servers with different implementations and transport methods.

## Features
- **Python Weather Server**: FastMCP-based weather server using National Weather Service API
- Streamable HTTP transport for modern MCP clients
- Health endpoints for monitoring and container orchestration
- Optional API key authentication patterns
- Container-ready with Docker support
- Azure Container Apps deployment examples

## Prerequisites
- Python 3.12+ (for Python weather server)
- uv package manager
- (Optional) Docker
- (Optional) Azure CLI for cloud deployment

## Quick Start

### Python Weather Server
Navigate to the `python/` directory and follow the setup instructions:

```bash
cd python
uv venv
uv sync
```

Run locally:
```bash
.venv/Scripts/uvicorn.exe app.main:app --reload --host 127.0.0.1 --port 8000
```

The MCP server will be available at `http://localhost:8000/mcp`


## MCP Client Configuration

### MCP Inspector (Recommended for Testing)
1. Install and run MCP Inspector:
```bash
npx @modelcontextprotocol/inspector
```

2. Connect using Streamable HTTP:
- **Transport**: Streamable HTTP  
- **URL**: `http://localhost:8000/mcp` (local) or your deployed URL

### VS Code MCP Configuration
For MCP clients that support configuration files, use:

```json
{
  "mcp": {
    "servers": {
      "weather-server": {
        "url": "http://localhost:8000/mcp",
        "type": "streamable-http"
      }
    }
  }
}
```

## Docker

### Python Weather Server
```bash
cd python
docker build -t mcp-weather-server .
docker run -p 8000:8000 mcp-weather-server
```

MCP endpoint: `http://localhost:8000/mcp`

## Available MCP Tools

### Weather Tools (Python Server)
The weather server provides these MCP tools using the National Weather Service API:

- **`get_alerts(state)`**: Get weather alerts for a US state
  - `state` (string): Two-letter state code (e.g., "MN", "CA", "TX")
  - Returns: Current weather alerts and warnings for the state

- **`get_forecast(latitude, longitude)`**: Get weather forecast for coordinates  
  - `latitude` (float): Location latitude
  - `longitude` (float): Location longitude
  - Returns: 5-day weather forecast with temperatures, conditions, and detailed descriptions

### Example Usage
```bash
# Test with MCP Inspector or any MCP client
{
  "method": "tools/call",
  "params": {
    "name": "get_alerts", 
    "arguments": {"state": "MN"}
  }
}
```

## Azure Container Apps Deployment

The Python weather server can be deployed to Azure Container Apps:

### Build and Deploy
```bash
# From the python/ directory
az acr build --registry <your-registry> --image mcp-weather-server:latest .

az containerapp update \
  --name weather-mcp-server \
  --resource-group <your-resource-group> \
  --image <your-registry>.azurecr.io/mcp-weather-server:latest
```

### Health Probes
Configure Azure Container Apps health probes:
- **Health probe path**: `/api/health`
- **Port**: 8000

See the `python/README.md` for detailed deployment instructions.

## Project Structure

```
mcp-server-hub/
├── python/                 # FastMCP weather server
│   ├── app/
│   │   ├── main.py        # Main MCP server with weather tools
│   │   └── __init__.py
│   ├── Dockerfile         # Container configuration
│   ├── pyproject.toml     # Python dependencies
│   ├── uv.lock           # Dependency lock file
│   └── README.md         # Detailed setup instructions
└── README.md             # This file
```

## Development

### Adding New Tools
To add new MCP tools to the Python weather server:

1. Add tool functions using the `@mcp.tool()` decorator
2. Follow the FastMCP documentation for tool definitions
3. Test with MCP Inspector before deployment

### Contributing
- Each server implementation should have its own directory
- Include comprehensive README.md files
- Provide Docker configurations for containerization
- Add health endpoints for monitoring

## Next Steps
- Add more specialized MCP servers (database tools, file operations, etc.)
- Implement authentication patterns
- Add integration tests
- Consider rate limiting for production use