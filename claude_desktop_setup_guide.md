# Claude Desktop Connection Guide for IoT Vulnerability Scanner

## Prerequisites

1. **Docker Desktop** installed and running
2. **Claude Desktop** installed
3. This IoT vulnerability scanner project cloned locally

## Step 1: Build the Docker Image

First, build the Docker container for the MCP server:

```bash
# Navigate to the project directory
cd /Users/kroeung/Desktop/iot-vuln-mcp

# Build the Docker image
docker build -t iot-security-scanner .
```

## Step 2: Configure Claude Desktop

### For macOS Users:

1. Open **Finder** 
2. Press `Cmd+Shift+H` to go to your Home folder
3. Navigate to: **Library** → **Application Support** → **Claude**
4. Create or edit the file `claude_desktop_config.json` with this content:

```json
{
  "mcpServers": {
    "iot-security-scanner": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "iot-security-scanner"]
    }
  }
}
```

### For Windows Users:

1. Press `Win+R`, type `%APPDATA%\Claude` and press Enter
2. Create or edit `claude_desktop_config.json` with the same content above

## Step 3: Restart Claude Desktop

Close Claude Desktop completely and reopen it. The MCP server should now be connected.

## Step 4: Verify Connection

Once Claude Desktop restarts, you can test the connection by asking Claude:

- "What IoT security scanning tools are available?"
- "Scan my security camera at 192.168.1.100"
- "Check my smart devices for vulnerabilities"

## Available Tools

Once connected, you'll have access to these security scanning tools:

1. **comprehensive_iot_scan** - Full vulnerability scan for IoT devices
2. **camera_vulnerability_assessment** - Specialized camera security testing
3. **rtsp_stream_analysis** - RTSP stream security analysis
4. **default_credential_test** - Default password testing
5. **firmware_analysis** - Firmware vulnerability assessment
6. **network_exposure_check** - Network service exposure analysis
7. **smart_home_protocol_test** - Smart home protocol security testing
8. **security_health_check** - Overall IoT ecosystem security check

## Example Usage

```
"Scan my security camera at 192.168.1.100 for vulnerabilities"
"Check if my smart thermostat has default passwords"
"Analyze my home network for IoT security risks"
"Test my IP camera's RTSP stream security"
```

## Troubleshooting

### Common Issues:

1. **"Docker not found"** - Ensure Docker Desktop is running
2. **"Claude can't connect"** - Restart Claude Desktop after config changes
3. **"Scanner not working"** - Check your device IP addresses are correct
4. **"Permission denied"** - Ensure Docker has proper permissions

### Verify Docker Build:

```bash
# Check if image was built successfully
docker images | grep iot-security-scanner

# Test the container manually
docker run -it --rm iot-security-scanner python3 verification_test.py
```

### Check Claude Logs:

- On macOS: `~/Library/Logs/Claude/`
- On Windows: `%APPDATA%\Claude\logs\`

## Security & Legal Notice

⚠️ **IMPORTANT**: Only scan devices you own or have explicit permission to test. Unauthorized scanning may be illegal in your jurisdiction.

- ✅ **Your own devices** - Yes!
- ✅ **Devices you manage** - With permission!
- ❌ **Neighbors' cameras** - No!
- ❌ **Public cameras** - No!
- ❌ **Work devices** - Only with written permission!

## Next Steps

After successful connection:

1. Test with a device you own (e.g., your router at 192.168.1.1)
2. Try different scan types to understand the capabilities
3. Review the scan results and implement security recommendations
4. Keep the scanner updated with `docker build -t iot-security-scanner .`

---

**Ready to secure your smart home? Just ask Claude to scan your devices!**
