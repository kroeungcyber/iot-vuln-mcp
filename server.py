#!/usr/bin/env python3
"""
Smart Home & IP Camera Vulnerability Scanner MCP Server
Specialized for IoT devices and security cameras with enhanced security features
"""

import asyncio
import json
import sqlite3
import subprocess
import re
import aiofiles
import aiosqlite
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import hashlib
import ipaddress

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions, ServerCapabilities
import mcp.types as types
import mcp.server.stdio

# Enhanced logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('iot_scanner.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("iot-vuln-scanner")

class IoTVulnerabilityScanner:
    def __init__(self):
        self.server = Server("iot-vuln-scanner")
        self.iot_signatures = {}
        self.scan_history = []
        self.setup_handlers()
        
        # Security controls
        self.max_scan_time = 300  # 5 minutes
        self.max_targets_per_scan = 5
        self.banned_targets = ['0.0.0.0', '255.255.255.255', '127.0.0.1']
    
    async def load_iot_signatures(self) -> Dict:
        """Load IoT device signatures and known vulnerabilities"""
        try:
            async with aiofiles.open('iot_signatures.json', 'r') as f:
                content = await f.read()
                return json.loads(content)
        except FileNotFoundError:
            logger.warning("iot_signatures.json not found, using default signatures")
            return self.get_default_signatures()
        except Exception as e:
            logger.error(f"Error loading signatures: {e}")
            return self.get_default_signatures()
    
    def get_default_signatures(self) -> Dict:
        """Default IoT device signatures with enhanced data"""
        return {
            "camera_manufacturers": {
                "hikvision": {
                    "ports": [80, 443, 554, 8000, 8080, 34567],
                    "default_credentials": [
                        {"username": "admin", "password": "12345"},
                        {"username": "admin", "password": "admin"}
                    ],
                    "vulnerabilities": ["CVE-2017-7921", "CVE-2021-36260"],
                    "rtsp_paths": ["/Streaming/Channels/101", "/cam/realmonitor"],
                    "web_paths": ["/", "/doc/page/login.asp"]
                },
                "dahua": {
                    "ports": [80, 443, 554, 37777, 37778],
                    "default_credentials": [
                        {"username": "admin", "password": "admin"},
                        {"username": "admin", "password": ""}
                    ],
                    "vulnerabilities": ["CVE-2021-33044", "CVE-2022-30563"],
                    "rtsp_paths": ["/cam/realmonitor", "live.sdp"],
                    "web_paths": ["/", "/cgi-bin/login.cgi"]
                },
                "axis": {
                    "ports": [80, 443, 554],
                    "default_credentials": [
                        {"username": "root", "password": "pass"},
                        {"username": "admin", "password": ""}
                    ],
                    "vulnerabilities": ["CVE-2018-10660"],
                    "rtsp_paths": ["/axis-media/media.amp", "live.sdp"],
                    "web_paths": ["/", "/view/view.shtml"]
                }
            },
            "iot_protocols": {
                "rtsp": {"port": 554, "security_risks": ["unencrypted_streams", "weak_authentication"]},
                "onvif": {"port": 80, "security_risks": ["information_disclosure", "weak_ws_security"]},
                "mqtt": {"port": 1883, "security_risks": ["unencrypted_communication", "no_authentication"]},
                "http": {"port": 80, "security_risks": ["clear_text_communication", "session_management"]},
                "https": {"port": 443, "security_risks": ["weak_ssl_configuration"]}
            },
            "common_vulnerabilities": {
                "default_credentials": {
                    "severity": "HIGH",
                    "impact": "Full device compromise",
                    "remediation": "Change default passwords immediately",
                    "cvss_score": 9.8
                },
                "unencrypted_streams": {
                    "severity": "MEDIUM", 
                    "impact": "Eavesdropping on video/audio",
                    "remediation": "Use encrypted protocols (RTSPS, HTTPS)",
                    "cvss_score": 5.9
                },
                "outdated_firmware": {
                    "severity": "HIGH",
                    "impact": "Known exploit vulnerability",
                    "remediation": "Update to latest firmware version",
                    "cvss_score": 8.2
                }
            }
        }
    
    def setup_handlers(self):
        """Set up MCP server handlers for IoT testing"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """List available IoT vulnerability scanning tools with enhanced descriptions"""
            return [
                types.Tool(
                    name="comprehensive_iot_scan",
                    description="Comprehensive vulnerability scan for IoT devices and cameras with detailed reporting",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "target": {
                                "type": "string", 
                                "description": "IP address or hostname of the IoT device"
                            },
                            "scan_intensity": {
                                "type": "string", 
                                "enum": ["quick", "deep", "stealth"], 
                                "default": "quick",
                                "description": "Scan intensity level"
                            },
                            "check_credentials": {
                                "type": "boolean",
                                "default": True,
                                "description": "Test for default credentials"
                            }
                        },
                        "required": ["target"]
                    }
                ),
                types.Tool(
                    name="camera_vulnerability_assessment",
                    description="Specialized security assessment for IP security cameras with brand detection",
                    inputSchema={
                        "type": "object", 
                        "properties": {
                            "target": {
                                "type": "string", 
                                "description": "Camera IP address or hostname"
                            },
                            "camera_type": {
                                "type": "string", 
                                "enum": ["auto", "hikvision", "dahua", "axis", "uniview", "generic"],
                                "description": "Camera manufacturer type"
                            },
                            "test_streams": {
                                "type": "boolean",
                                "default": True,
                                "description": "Test RTSP stream security"
                            }
                        },
                        "required": ["target"]
                    }
                ),
                types.Tool(
                    name="rtsp_stream_analysis",
                    description="Comprehensive RTSP stream security analysis with authentication testing",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "target": {
                                "type": "string", 
                                "description": "Camera IP or RTSP URL"
                            },
                            "check_authentication": {
                                "type": "boolean", 
                                "default": True,
                                "description": "Test stream authentication"
                            },
                            "test_common_paths": {
                                "type": "boolean",
                                "default": True,
                                "description": "Test common RTSP paths"
                            }
                        },
                        "required": ["target"]
                    }
                ),
                types.Tool(
                    name="default_credential_test",
                    description="Advanced default credential testing with manufacturer-specific credentials",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "target": {
                                "type": "string", 
                                "description": "Device IP address"
                            },
                            "device_type": {
                                "type": "string", 
                                "description": "Specific device type for targeted testing"
                            },
                            "protocol": {
                                "type": "string",
                                "enum": ["http", "https", "both"],
                                "default": "both",
                                "description": "Protocol to test"
                            }
                        },
                        "required": ["target"]
                    }
                ),
                types.Tool(
                    name="firmware_analysis",
                    description="Firmware vulnerability assessment and version checking",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "target": {
                                "type": "string", 
                                "description": "Device IP address"
                            },
                            "manufacturer": {
                                "type": "string", 
                                "description": "Device manufacturer for CVE lookup"
                            },
                            "check_cves": {
                                "type": "boolean",
                                "default": True,
                                "description": "Check for known CVEs"
                            }
                        },
                        "required": ["target"]
                    }
                ),
                types.Tool(
                    name="network_exposure_check",
                    description="Network service exposure analysis with risk assessment",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "target": {
                                "type": "string", 
                                "description": "Device IP address"
                            },
                            "check_upnp": {
                                "type": "boolean", 
                                "default": True,
                                "description": "Check UPNP services"
                            },
                            "port_range": {
                                "type": "string",
                                "default": "1-10000",
                                "description": "Port range to scan"
                            }
                        },
                        "required": ["target"]
                    }
                ),
                types.Tool(
                    name="smart_home_protocol_test",
                    description="Smart home protocol security testing (MQTT, Zigbee, Z-Wave)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "target": {
                                "type": "string", 
                                "description": "Gateway IP or network range"
                            },
                            "protocol": {
                                "type": "string", 
                                "enum": ["mqtt", "zigbee", "zwave", "all"],
                                "description": "Protocol to test"
                            },
                            "check_encryption": {
                                "type": "boolean",
                                "default": True,
                                "description": "Check protocol encryption"
                            }
                        },
                        "required": ["target"]
                    }
                ),
                types.Tool(
                    name="security_health_check",
                    description="Overall security health check for IoT ecosystem",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "network_range": {
                                "type": "string", 
                                "description": "Network range to scan (e.g., 192.168.1.0/24)"
                            },
                            "check_common_ports": {
                                "type": "boolean",
                                "default": True,
                                "description": "Scan common IoT ports"
                            }
                        },
                        "required": ["network_range"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
            """Handle IoT vulnerability scanning tool execution with enhanced security"""
            try:
                # Security validation
                validation_error = await self.validate_scan_request(name, arguments)
                if validation_error:
                    return [types.TextContent(type="text", text=f"Security Validation Failed: {validation_error}")]
                
                # Legal warning
                legal_warning = await self.get_legal_warning()
                
                tool_handlers = {
                    "comprehensive_iot_scan": self.comprehensive_iot_scan,
                    "camera_vulnerability_assessment": self.camera_vulnerability_assessment,
                    "rtsp_stream_analysis": self.rtsp_stream_analysis,
                    "default_credential_test": self.default_credential_test,
                    "firmware_analysis": self.firmware_analysis,
                    "network_exposure_check": self.network_exposure_check,
                    "smart_home_protocol_test": self.smart_home_protocol_test,
                    "security_health_check": self.security_health_check
                }
                
                if name in tool_handlers:
                    result = await tool_handlers[name](arguments)
                    # Add legal warning to results
                    if legal_warning and not result[0].text.startswith("Error"):
                        result[0].text = legal_warning + "\n\n" + result[0].text
                    return result
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}")
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def validate_scan_request(self, tool_name: str, arguments: Dict[str, Any]) -> Optional[str]:
        """Validate scan requests for security and safety"""
        target = arguments.get('target') or arguments.get('network_range')
        
        if not target:
            return "No target specified"
        
        # Check for banned targets
        if target in self.banned_targets:
            return f"Scanning {target} is not permitted"
        
        # Validate IP format
        try:
            if '/' in target:
                network = ipaddress.ip_network(target, strict=False)
                if network.num_addresses > 256:
                    return "Network range too large (max /24)"
            else:
                ipaddress.ip_address(target)
        except ValueError:
            return f"Invalid IP address or network range: {target}"
        
        # Rate limiting
        recent_scans = [s for s in self.scan_history if datetime.now().timestamp() - s['timestamp'] < 300]
        if len(recent_scans) > 10:
            return "Rate limit exceeded - please wait before scanning again"
        
        # Add to scan history
        self.scan_history.append({
            'tool': tool_name,
            'target': target,
            'timestamp': datetime.now().timestamp()
        })
        
        return None
    
    async def get_legal_warning(self) -> str:
        """Get legal warning message"""
        try:
            async with aiofiles.open('legal_warning.md', 'r') as f:
                content = await f.read()
                # Extract first section for brevity
                return content.split('##')[0].strip()
        except:
            return "⚠️ LEGAL WARNING: Only test devices you own or have explicit permission to scan. Unauthorized testing may be illegal."
    
    async def run_command(self, command: List[str], timeout: int = 60) -> str:
        """Run a shell command with timeout and enhanced security"""
        try:
            logger.info(f"Executing: {' '.join(command)}")
            result = await asyncio.wait_for(
                asyncio.create_subprocess_exec(
                    *command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                ),
                timeout=timeout
            )
            stdout, stderr = await result.communicate()
            
            if result.returncode == 0:
                return stdout.decode('utf-8', errors='ignore')
            else:
                return f"Error: {stderr.decode('utf-8', errors='ignore')}"
                
        except asyncio.TimeoutExpired:
            return "Error: Command timed out"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def comprehensive_iot_scan(self, arguments: Dict[str, Any]) -> list[types.TextContent]:
        """Enhanced comprehensive IoT device vulnerability scan"""
        target = arguments["target"]
        intensity = arguments.get("scan_intensity", "quick")
        check_creds = arguments.get("check_credentials", True)
        
        scan_results = [f"🔍 Comprehensive IoT Vulnerability Scan for {target}\n"]
        scan_results.append(f"📊 Scan Intensity: {intensity}\n")
        scan_results.append("="*60 + "\n")
        
        # Phase 1: Network Discovery
        scan_results.append("\n🌐 NETWORK DISCOVERY:\n")
        ports = "1-1000,554,8000,8080,37777,34567,1883,8883" if intensity == "deep" else "80,443,554,8000,1883"
        nmap_command = ["nmap", "-T4", "-sV", "-sC", "-p", ports, target]
        if intensity == "stealth":
            nmap_command.extend(["-T2", "-sS"])
        
        port_scan = await self.run_command(nmap_command)
        scan_results.append(port_scan)
        
        # Phase 2: Service Analysis
        scan_results.append("\n🔧 SERVICE ANALYSIS:\n")
        services = await self.analyze_services(target, port_scan)
        scan_results.extend(services)
        
        # Phase 3: Vulnerability Assessment
        scan_results.append("\n⚠️ VULNERABILITY ASSESSMENT:\n")
        
        vuln_checks = [
            ("Default Credentials", await self.check_default_credentials(target) if check_creds else "Skipped"),
            ("RTSP Security", await self.check_rtsp_security(target)),
            ("Web Interface", await self.check_web_interface(target)),
            ("Firmware Analysis", await self.check_firmware_version(target))
        ]
        
        for check_name, result in vuln_checks:
            scan_results.append(f"\n{check_name}:\n{result}\n")
        
        # Phase 4: Risk Summary
        scan_results.append("\n📋 RISK SUMMARY:\n")
        summary = await self.generate_risk_summary(target, scan_results)
        scan_results.append(summary)
        
        # Save to database
        await self.save_scan_result(target, "comprehensive_scan", "\n".join(scan_results))
        
        return [types.TextContent(type="text", text="".join(scan_results))]
    
    async def camera_vulnerability_assessment(self, arguments: Dict[str, Any]) -> list[types.TextContent]:
        """Enhanced specialized assessment for IP security cameras"""
        target = arguments["target"]
        camera_type = arguments.get("camera_type", "auto")
        test_streams = arguments.get("test_streams", True)
        
        results = [f"📹 IP Camera Vulnerability Assessment for {target}\n"]
        results.append(f"📷 Camera Type: {camera_type}\n")
        results.append("="*60 + "\n")
        
        # Camera-specific vulnerability checks
        results.append("\n🔍 CAMERA-SPECIFIC CHECKS:\n")
        
        # Add placeholder for camera assessment logic
        results.append("Camera vulnerability assessment would include:\n")
        results.append("- Manufacturer-specific vulnerability checks\n")
        results.append("- RTSP stream security analysis\n")
        results.append("- Web interface security testing\n")
        results.append("- Default credential testing\n")
        results.append("- Firmware version analysis\n")
        
        return [types.TextContent(type="text", text="".join(results))]

    # Placeholder methods for other tool implementations
    async def rtsp_stream_analysis(self, arguments: Dict[str, Any]) -> list[types.TextContent]:
        return [types.TextContent(type="text", text="RTSP Stream Analysis - Implementation pending")]
    
    async def default_credential_test(self, arguments: Dict[str, Any]) -> list[types.TextContent]:
        return [types.TextContent(type="text", text="Default Credential Test - Implementation pending")]
    
    async def firmware_analysis(self, arguments: Dict[str, Any]) -> list[types.TextContent]:
        return [types.TextContent(type="text", text="Firmware Analysis - Implementation pending")]
    
    async def network_exposure_check(self, arguments: Dict[str, Any]) -> list[types.TextContent]:
        return [types.TextContent(type="text", text="Network Exposure Check - Implementation pending")]
    
    async def smart_home_protocol_test(self, arguments: Dict[str, Any]) -> list[types.TextContent]:
        return [types.TextContent(type="text", text="Smart Home Protocol Test - Implementation pending")]
    
    async def security_health_check(self, arguments: Dict[str, Any]) -> list[types.TextContent]:
        return [types.TextContent(type="text", text="Security Health Check - Implementation pending")]
    
    # Placeholder helper methods
    async def analyze_services(self, target: str, port_scan: str) -> List[str]:
        return ["Service analysis would be implemented here"]
    
    async def check_default_credentials(self, target: str) -> str:
        return "Default credential check would be implemented here"
    
    async def check_rtsp_security(self, target: str) -> str:
        return "RTSP security check would be implemented here"
    
    async def check_web_interface(self, target: str) -> str:
        return "Web interface check would be implemented here"
    
    async def check_firmware_version(self, target: str) -> str:
        return "Firmware version check would be implemented here"
    
    async def generate_risk_summary(self, target: str, scan_results: List[str]) -> str:
        return "Risk summary would be generated here"
    
    async def save_scan_result(self, target: str, scan_type: str, results: str):
        pass


async def main():
    """Main function to run the MCP server"""
    scanner = IoTVulnerabilityScanner()
    await scanner.load_iot_signatures()
    
    # Run the MCP server
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await scanner.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="iot-vuln-scanner",
                server_version="1.0.0",
                capabilities=scanner.server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
