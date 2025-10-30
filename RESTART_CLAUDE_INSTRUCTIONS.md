# How to Connect IoT-Vuln-MCP to Claude Desktop

## ✅ Setup Complete

The MCP server has been successfully configured and the Docker image has been rebuilt with the correct imports.

## 🔄 Next Steps - Restart Claude Desktop

1. **Quit Claude Desktop completely**:
   - Press `Cmd + Q` to quit Claude Desktop
   - Or right-click the Claude icon in the dock and select "Quit"
   - Make sure it's fully closed (not just the window)

2. **Reopen Claude Desktop**:
   - Launch Claude Desktop from Applications or Spotlight
   - Wait for it to fully load

3. **Verify the Connection**:
   - Look for a small plug icon (🔌) or MCP indicator in the Claude interface
   - The MCP server should now be available

4. **Test the Connection**:
   Try asking Claude:
   ```
   What IoT security scanning tools do you have available?
   ```
   
   Or:
   ```
   Can you help me scan an IoT device for vulnerabilities?
   ```

## 📋 Configuration Files

Your configuration is located at:
- **Config File**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Docker Image**: `iot-security-scanner:latest`

## 🔍 Troubleshooting

If the connection still doesn't work:

1. **Check the logs** after restarting:
   ```bash
   cat ~/Library/Logs/Claude/mcp-server-iot-security-scanner.log
   ```

2. **Verify Docker is running**:
   ```bash
   docker ps
   ```

3. **Test the server manually**:
   ```bash
   docker run --rm iot-security-scanner python3 -c "from server import main; print('Server OK')"
   ```

4. **Check configuration format**:
   ```bash
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```
   
   Should show:
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

## 🎯 Available Tools Once Connected

1. **comprehensive_iot_scan** - Full vulnerability assessment
2. **camera_vulnerability_assessment** - IP camera security testing
3. **rtsp_stream_analysis** - Video stream security testing
4. **default_credential_test** - Credential testing
5. **firmware_analysis** - Firmware version analysis
6. **network_exposure_check** - Service exposure analysis
7. **smart_home_protocol_test** - Protocol security testing
8. **security_health_check** - Overall security assessment

## ⚠️ Legal Notice

Only use these tools on devices you own or have explicit permission to test. Unauthorized security testing may be illegal.
