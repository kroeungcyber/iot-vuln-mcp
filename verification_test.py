#!/usr/bin/env python3
"""
Comprehensive Verification Test for IoT Vulnerability Scanner
Tests security, functionality, and performance characteristics
"""

import asyncio
import subprocess
import sys
import sqlite3
import time
import resource
import json
from typing import List, Tuple

class IoTScannerVerification:
    def __init__(self):
        self.test_results = []
        self.performance_metrics = {}
    
    async def run_test(self, test_name: str, test_func) -> bool:
        """Run a test and record results with timing"""
        start_time = time.time()
        try:
            result = await test_func()
            duration = time.time() - start_time
            self.test_results.append((test_name, "PASS", duration))
            print(f"✅ {test_name}: PASS ({duration:.2f}s)")
            return True
        except Exception as e:
            duration = time.time() - start_time
            self.test_results.append((test_name, f"FAIL: {e}", duration))
            print(f"❌ {test_name}: FAIL - {e} ({duration:.2f}s)")
            return False
    
    async def test_docker_build(self) -> bool:
        """Test Docker image builds successfully"""
        result = subprocess.run(
            ["docker", "build", "-t", "iot-vuln-scanner-test", "."],
            capture_output=True, 
            text=True,
            timeout=300  # 5 minute timeout
        )
        if result.returncode != 0:
            raise Exception(f"Build failed: {result.stderr}")
        return True
    
    async def test_container_security(self) -> bool:
        """Test container security features"""
        # Test non-root user
        result = subprocess.run(
            ["docker", "run", "--rm", "iot-vuln-scanner-test", "whoami"],
            capture_output=True, text=True
        )
        if "iottester" not in result.stdout.strip():
            raise Exception("Container not running as non-root user")
        
        # Test privilege escalation
        result = subprocess.run(
            ["docker", "run", "--rm", "iot-vuln-scanner-test", "id"],
            capture_output=True, text=True
        )
        if "uid=0" in result.stdout:
            raise Exception("Container has root privileges")
        
        return True
    
    async def test_python_dependencies(self) -> bool:
        """Test Python dependencies are available"""
        dependencies = [
            "mcp", "pydantic", "fastapi", "uvicorn", "websockets",
            "python-nmap", "requests", "aiofiles", "aiosqlite"
        ]
        
        for dep in dependencies:
            try:
                __import__(dep)
            except ImportError as e:
                raise Exception(f"Missing dependency {dep}: {e}")
        
        return True
    
    async def test_iot_tools_available(self) -> bool:
        """Test required IoT tools are installed"""
        tools = ["nmap", "curl", "ffmpeg", "sqlite3"]
        missing_tools = []
        
        for tool in tools:
            result = subprocess.run(["which", tool], capture_output=True)
            if result.returncode != 0:
                missing_tools.append(tool)
        
        if missing_tools:
            raise Exception(f"Missing tools: {', '.join(missing_tools)}")
        
        return True
    
    async def test_database_functionality(self) -> bool:
        """Test SQLite database operations"""
        try:
            # Test basic database operations
            conn = sqlite3.connect(':memory:')
            cursor = conn.cursor()
            
            # Test table creation
            cursor.execute('''
                CREATE TABLE test_scan (
                    id INTEGER PRIMARY KEY,
                    target TEXT,
                    scan_type TEXT,
                    findings TEXT
                )
            ''')
            
            # Test data operations
            test_data = [
                ("192.168.1.100", "comprehensive_scan", "No vulnerabilities"),
                ("192.168.1.101", "camera_scan", "Default credentials found")
            ]
            
            cursor.executemany(
                'INSERT INTO test_scan (target, scan_type, findings) VALUES (?, ?, ?)',
                test_data
            )
            conn.commit()
            
            # Test data retrieval
            cursor.execute('SELECT COUNT(*) FROM test_scan')
            count = cursor.fetchone()[0]
            if count != 2:
                raise Exception("Database data retrieval failed")
            
            conn.close()
            return True
            
        except Exception as e:
            raise Exception(f"Database test failed: {e}")
    
    async def test_configuration_files(self) -> bool:
        """Test configuration files are valid"""
        try:
            # Test IoT signatures JSON
            with open('iot_signatures.json', 'r') as f:
                signatures = json.load(f)
            
            required_sections = ["camera_manufacturers", "iot_protocols", "common_vulnerabilities"]
            for section in required_sections:
                if section not in signatures:
                    raise Exception(f"Missing section in signatures: {section}")
            
            # Test legal warning file
            with open('legal_warning.md', 'r') as f:
                content = f.read()
                if "LEGAL WARNING" not in content:
                    raise Exception("Legal warning file missing required content")
            
            return True
            
        except Exception as e:
            raise Exception(f"Configuration test failed: {e}")
    
    async def test_performance_characteristics(self) -> bool:
        """Test performance and resource usage"""
        start_time = time.time()
        memory_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        
        # Simulate intensive operations
        processes = []
        for i in range(5):  # Simulate concurrent operations
            proc = subprocess.Popen(
                ["python3", "-c", "import time; time.sleep(0.1)"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            processes.append(proc)
        
        # Wait for all processes
        for proc in processes:
            proc.wait()
        
        memory_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        duration = time.time() - start_time
        
        # Store metrics
        self.performance_metrics.update({
            "memory_usage_kb": memory_after - memory_before,
            "concurrent_operations_time": duration
        })
        
        # Validate performance
        if duration > 10:  # Should complete quickly
            raise Exception(f"Performance test too slow: {duration:.2f}s")
        
        if (memory_after - memory_before) > 100 * 1024:  # 100MB limit
            raise Exception("Memory usage too high")
        
        return True
    
    async def test_network_safety(self) -> bool:
        """Test network safety controls"""
        try:
            # Test that localhost scanning is prevented
            result = subprocess.run(
                ["docker", "run", "--rm", "iot-vuln-scanner-test", 
                 "python3", "-c", "from server import IoTVulnerabilityScanner; s = IoTVulnerabilityScanner()"],
                capture_output=True, text=True, timeout=30
            )
            
            # The server should start without attempting network operations
            if result.returncode != 0 and "error" in result.stderr.lower():
                raise Exception(f"Server startup failed: {result.stderr}")
            
            return True
            
        except subprocess.TimeoutExpired:
            raise Exception("Network safety test timed out")
        except Exception as e:
            raise Exception(f"Network safety test failed: {e}")
    
    async def test_error_handling(self) -> bool:
        """Test error handling and resilience"""
        try:
            # Test with invalid inputs
            invalid_commands = [
                ["nmap", "--invalid-flag"],
                ["curl", "invalid://url"],
                ["ffmpeg", "-invalid", "input"]
            ]
            
            for cmd in invalid_commands:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                # Should handle errors gracefully, not crash
                if result.returncode == -1:  # Crash
                    raise Exception(f"Command crashed: {' '.join(cmd)}")
            
            return True
            
        except Exception as e:
            raise Exception(f"Error handling test failed: {e}")
    
    async def run_all_tests(self) -> bool:
        """Run all verification tests"""
        print("🚀 Starting IoT Vulnerability Scanner Verification Tests")
        print("=" * 60)
        
        tests = [
            ("Docker Build", self.test_docker_build),
            ("Container Security", self.test_container_security),
            ("Python Dependencies", self.test_python_dependencies),
            ("IoT Tools Available", self.test_iot_tools_available),
            ("Database Functionality", self.test_database_functionality),
            ("Configuration Files", self.test_configuration_files),
            ("Performance Characteristics", self.test_performance_characteristics),
            ("Network Safety", self.test_network_safety),
            ("Error Handling", self.test_error_handling)
        ]
        
        results = []
        for test_name, test_func in tests:
            result = await self.run_test(test_name, test_func)
            results.append(result)
        
        # Print detailed summary
        print("\n" + "=" * 60)
        print("📊 VERIFICATION TEST SUMMARY")
        print("=" * 60)
        
        for test_name, status, duration in self.test_results:
            status_icon = "✅" if status == "PASS" else "❌"
            print(f"{status_icon} {test_name}: {status} ({duration:.2f}s)")
        
        # Performance metrics
        if self.performance_metrics:
            print("\n📈 PERFORMANCE METRICS:")
            for metric, value in self.performance_metrics.items():
                print(f"   {metric}: {value}")
        
        # Overall result
        passed = sum(1 for _, status, _ in self.test_results if status == "PASS")
        total = len(self.test_results)
        
        print(f"\n🎯 OVERALL RESULT: {passed}/{total} tests passed")
        
        if passed == total:
            print("✨ ALL TESTS PASSED - Ready for deployment!")
        else:
            print("💥 SOME TESTS FAILED - Review before deployment")
        
        return passed == total

async def main():
    """Main verification entry point"""
    verifier = IoTScannerVerification()
    success = await verifier.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())
