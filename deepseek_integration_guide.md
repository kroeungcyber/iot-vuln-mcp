# Multi-LLM Integration Guide for IoT Vulnerability Scanner MCP Server

This guide explains how to integrate the IoT Vulnerability Scanner MCP server with multiple LLMs including DeepSeek and ChatGPT.

## Prerequisites

- DeepSeek LLM installed and configured
- Python 3.8+ installed
- Git installed
- Network access for IoT device scanning

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/kroeungcyber/iot-vuln-mcp.git
cd iot-vuln-mcp
```

### 2. Install Dependencies
```bash
# For full functionality (recommended)
pip install -r requirements.txt

# OR for minimal dependencies (compatible version)
pip install -r requirements_compatible.txt
```

### 3. Verify Installation
```bash
# Test the server starts correctly
python server.py

# Run compliance tests
python mcp_compliance_test.py
```

## DeepSeek Configuration

### Option 1: Direct Integration (If DeepSeek supports MCP)

If DeepSeek has built-in MCP support, add this to your DeepSeek configuration:

```json
{
  "mcpServers": {
    "iot-vuln-scanner": {
      "command": "python",
      "args": ["/path/to/iot-vuln-mcp/server.py"],
      "env": {
        "PYTHONPATH": "/path/to/iot-vuln-mcp"
      }
    }
  }
}
```

### Option 2: Claude Desktop Bridge (Recommended)

Since DeepSeek may not have direct MCP support yet, use Claude Desktop as a bridge:

1. **Install Claude Desktop** from Anthropic
2. **Configure Claude Desktop** with the IoT scanner:

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "iot-vuln-scanner": {
      "command": "python",
      "args": ["/Users/kroeung/Desktop/iot-vuln-mcp/server.py"],
      "cwd": "/Users/kroeung/Desktop/iot-vuln-mcp"
    }
  }
}
```

3. **Use DeepSeek with Claude Desktop** - DeepSeek can access the tools through Claude Desktop's MCP bridge

### Option 3: API Gateway Approach

Create a simple REST API wrapper:

```python
# api_gateway.py
from fastapi import FastAPI
import subprocess
import json

app = FastAPI()

@app.post("/scan")
async def scan_device(target: str, scan_type: str = "comprehensive"):
    """API endpoint that DeepSeek can call"""
    result = subprocess.run([
        "python", "server.py", "--target", target, "--type", scan_type
    ], capture_output=True, text=True)
    
    return {"result": result.stdout}
```

## Usage Examples

Once integrated, DeepSeek can use commands like:

```
"Scan my IP camera at 192.168.1.100 for vulnerabilities"
"Perform a comprehensive IoT security assessment on my network"
"Check if my smart home devices have default credentials"
```

## Available Tools for DeepSeek

The MCP server provides these tools that DeepSeek can access:

1. **comprehensive_iot_scan** - Full vulnerability assessment
2. **camera_vulnerability_assessment** - IP camera security testing
3. **rtsp_stream_analysis** - RTSP stream security analysis
4. **default_credential_test** - Default password testing
5. **firmware_analysis** - Firmware vulnerability checking
6. **network_exposure_check** - Network service analysis
7. **smart_home_protocol_test** - Smart home protocol security
8. **security_health_check** - Overall security assessment

## Troubleshooting

### Common Issues:

1. **Permission Errors**:
   ```bash
   chmod +x server.py
   ```

2. **Dependency Conflicts**:
   ```bash
   pip install -r requirements_compatible.txt
   ```

3. **Network Access**:
   - Ensure DeepSeek has network permissions
   - Test with localhost devices first

4. **MCP Connection**:
   ```bash
   # Test server manually
   python server.py
   # Should show server starting without errors
   ```

### Testing Integration:

```bash
# Test basic functionality
python basic_functionality_test.py

# Test MCP compliance
python mcp_compliance_test.py

# Test server demo
python server_demo_test.py
```

## Security Considerations

⚠️ **Important Security Notes**:

- Only scan devices you own or have permission to test
- The server includes legal warnings and safety checks
- Network scanning may trigger security systems
- Use responsibly and ethically

## ChatGPT Integration

### Option 1: OpenAI GPTs with Actions (Recommended)

Create a custom GPT with API actions:

1. **Create a new GPT** in OpenAI GPTs
2. **Configure Actions** with OpenAPI schema:

```yaml
openapi: 3.1.0
info:
  title: IoT Vulnerability Scanner API
  description: Security scanning tools for IoT devices and cameras
  version: 1.0.0
servers:
  - url: http://localhost:8000
paths:
  /scan/comprehensive:
    post:
      operationId: comprehensiveScan
      summary: Comprehensive IoT vulnerability scan
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                target:
                  type: string
                  description: IP address or hostname to scan
                scan_intensity:
                  type: string
                  enum: [quick, deep, stealth]
                  default: quick
                check_credentials:
                  type: boolean
                  default: true
      responses:
        '200':
          description: Scan results
  /scan/camera:
    post:
      operationId: cameraScan
      summary: IP camera vulnerability assessment
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                target:
                  type: string
                  description: Camera IP address
                camera_type:
                  type: string
                  enum: [auto, hikvision, dahua, axis, uniview, generic]
                  default: auto
                test_streams:
                  type: boolean
                  default: true
      responses:
        '200':
          description: Camera scan results
```

3. **Start the API Gateway**:
```bash
python deepseek_api_gateway.py
```

### Option 2: ChatGPT Plugins (Legacy)

For ChatGPT plugins support:

1. **Create plugin manifest** (`ai-plugin.json`):
```json
{
  "schema_version": "v1",
  "name_for_human": "IoT Vulnerability Scanner",
  "name_for_model": "iot_vulnerability_scanner",
  "description_for_human": "Security scanning tools for IoT devices and cameras",
  "description_for_model": "Tools for scanning IoT devices, IP cameras, and smart home devices for security vulnerabilities",
  "auth": {
    "type": "none"
  },
  "api": {
    "type": "openapi",
    "url": "http://localhost:8000/openapi.json",
    "is_user_authenticated": false
  },
  "logo_url": "http://localhost:8000/logo.png",
  "contact_email": "support@example.com",
  "legal_info_url": "http://localhost:8000/legal"
}
```

2. **Configure the plugin** in ChatGPT interface

### Option 3: Custom Instructions

Add these custom instructions to ChatGPT:

```
You have access to IoT vulnerability scanning tools through the API gateway. When users ask about:

- Scanning IoT devices or cameras
- Checking for security vulnerabilities
- Testing default credentials
- Analyzing network security

Use the available API endpoints to perform security scans. Always include legal warnings and ensure users only scan devices they own or have permission to test.
```

## Available Tools for All LLMs

The MCP server provides these tools that any LLM can access:

1. **comprehensive_iot_scan** - Full vulnerability assessment
2. **camera_vulnerability_assessment** - IP camera security testing
3. **rtsp_stream_analysis** - RTSP stream security analysis
4. **default_credential_test** - Default password testing
5. **firmware_analysis** - Firmware vulnerability checking
6. **network_exposure_check** - Network service analysis
7. **smart_home_protocol_test** - Smart home protocol security
8. **security_health_check** - Overall security assessment

## Usage Examples for ChatGPT

Once integrated, ChatGPT can use commands like:

```
"Scan my IP camera at 192.168.1.100 for vulnerabilities"
"Perform a comprehensive IoT security assessment on my network"
"Check if my smart home devices have default credentials"
"Analyze the RTSP stream security of my security camera"
```

## Troubleshooting

### Common Issues:

1. **Permission Errors**:
   ```bash
   chmod +x server.py
   ```

2. **Dependency Conflicts**:
   ```bash
   pip install -r requirements_compatible.txt
   ```

3. **Network Access**:
   - Ensure the LLM has network permissions
   - Test with localhost devices first

4. **MCP Connection**:
   ```bash
   # Test server manually
   python server.py
   # Should show server starting without errors
   ```

### Testing Integration:

```bash
# Test basic functionality
python basic_functionality_test.py

# Test MCP compliance
python mcp_compliance_test.py

# Test server demo
python server_demo_test.py

# Test API gateway
python deepseek_api_gateway.py
```

## Security Considerations

⚠️ **Important Security Notes**:

- Only scan devices you own or have permission to test
- The server includes legal warnings and safety checks
- Network scanning may trigger security systems
- Use responsibly and ethically

## Support

For integration issues:
1. Check the MCP compliance test results
2. Verify Python dependencies are installed
3. Ensure the LLM has proper network access
4. Test with the provided demo scripts

The server is designed to be LLM-agnostic and should work seamlessly with any MCP-compatible system, including DeepSeek, ChatGPT, and other LLMs.
