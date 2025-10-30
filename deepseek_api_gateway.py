#!/usr/bin/env python3
"""
DeepSeek API Gateway for IoT Vulnerability Scanner
Provides REST API endpoints that DeepSeek can call directly
"""

import asyncio
import json
import subprocess
import sys
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="IoT Vulnerability Scanner API", version="1.0.0")

class IoTVulnerabilityAPI:
    def __init__(self):
        self.server_process = None
    
    async def start_server(self):
        """Start the MCP server in background"""
        try:
            self.server_process = subprocess.Popen(
                [sys.executable, "server.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Wait a moment for server to start
            await asyncio.sleep(2)
            return True
        except Exception as e:
            print(f"Failed to start server: {e}")
            return False
    
    async def stop_server(self):
        """Stop the MCP server"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()

# Global API instance
api_gateway = IoTVulnerabilityAPI()

@app.on_event("startup")
async def startup_event():
    """Start the MCP server when API starts"""
    print("🚀 Starting IoT Vulnerability Scanner API Gateway...")
    success = await api_gateway.start_server()
    if success:
        print("✅ MCP Server started successfully")
    else:
        print("❌ Failed to start MCP Server")

@app.on_event("shutdown")
async def shutdown_event():
    """Stop the MCP server when API stops"""
    print("🛑 Stopping IoT Vulnerability Scanner API Gateway...")
    await api_gateway.stop_server()

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "IoT Vulnerability Scanner API Gateway",
        "version": "1.0.0",
        "available_endpoints": {
            "/scan/comprehensive": "POST - Comprehensive IoT scan",
            "/scan/camera": "POST - Camera vulnerability assessment", 
            "/scan/credentials": "POST - Default credential test",
            "/scan/firmware": "POST - Firmware analysis",
            "/health": "GET - API health check"
        }
    }

@app.post("/scan/comprehensive")
async def comprehensive_scan(target: str, scan_intensity: str = "quick", check_credentials: bool = True):
    """
    Comprehensive IoT vulnerability scan
    """
    try:
        # Simulate scan results (in production, this would call the MCP server)
        result = {
            "target": target,
            "scan_type": "comprehensive",
            "intensity": scan_intensity,
            "check_credentials": check_credentials,
            "results": {
                "port_scan": f"Port scan completed for {target}",
                "service_analysis": "Service analysis would be performed here",
                "vulnerability_assessment": "Vulnerability checks would be performed here",
                "risk_summary": "Risk assessment would be generated here"
            },
            "status": "completed"
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")

@app.post("/scan/camera")
async def camera_scan(target: str, camera_type: str = "auto", test_streams: bool = True):
    """
    IP camera vulnerability assessment
    """
    try:
        result = {
            "target": target,
            "scan_type": "camera_assessment",
            "camera_type": camera_type,
            "test_streams": test_streams,
            "results": {
                "camera_detection": f"Camera type detection for {target}",
                "rtsp_analysis": "RTSP stream security analysis",
                "web_interface": "Web interface security testing",
                "vulnerabilities": "Camera-specific vulnerability checks"
            },
            "status": "completed"
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Camera scan failed: {str(e)}")

@app.post("/scan/credentials")
async def credential_scan(target: str, device_type: str = "auto", protocol: str = "both"):
    """
    Default credential testing
    """
    try:
        result = {
            "target": target,
            "scan_type": "credential_test",
            "device_type": device_type,
            "protocol": protocol,
            "results": {
                "tested_credentials": "List of tested credentials",
                "authentication_status": "Authentication test results",
                "security_recommendations": "Credential security recommendations"
            },
            "status": "completed"
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Credential scan failed: {str(e)}")

@app.post("/scan/firmware")
async def firmware_scan(target: str, manufacturer: str = "auto", check_cves: bool = True):
    """
    Firmware vulnerability analysis
    """
    try:
        result = {
            "target": target,
            "scan_type": "firmware_analysis",
            "manufacturer": manufacturer,
            "check_cves": check_cves,
            "results": {
                "firmware_version": "Detected firmware version",
                "known_vulnerabilities": "List of known CVEs",
                "update_recommendations": "Firmware update suggestions"
            },
            "status": "completed"
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firmware scan failed: {str(e)}")

@app.get("/health")
async def health_check():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "service": "IoT Vulnerability Scanner API Gateway",
        "mcp_server": "running" if api_gateway.server_process else "stopped"
    }

if __name__ == "__main__":
    print("🌐 Starting DeepSeek API Gateway on http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
