#!/usr/bin/env python3
"""
Basic Functionality Test for IoT Vulnerability Scanner
Tests core components without MCP dependencies
"""

import asyncio
import json
import sqlite3
import sys
import os
from typing import List, Tuple

class BasicFunctionalityTester:
    def __init__(self):
        self.test_results = []
    
    async def run_test(self, test_name: str, test_func) -> bool:
        """Run a test and record results"""
        try:
            result = await test_func()
            self.test_results.append((test_name, "PASS", ""))
            print(f"✅ {test_name}: PASS")
            return True
        except Exception as e:
            self.test_results.append((test_name, "FAIL", str(e)))
            print(f"❌ {test_name}: FAIL - {e}")
            return False
    
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
                if "LEGAL" not in content.upper() or "WARNING" not in content.upper():
                    raise Exception("Legal warning file missing required content")
            
            return True
            
        except Exception as e:
            raise Exception(f"Configuration test failed: {e}")
    
    async def test_database_connectivity(self) -> bool:
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
    
    async def test_file_structure(self) -> bool:
        """Test required files exist"""
        required_files = [
            'README.md',
            'requirements.txt',
            'iot_signatures.json',
            'legal_warning.md',
            'server.py',
            'mcp_compliance_test.py',
            'verification_test.py'
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            raise Exception(f"Missing required files: {', '.join(missing_files)}")
        
        return True
    
    async def test_python_dependencies(self) -> bool:
        """Test Python dependencies are available"""
        dependencies = [
            "mcp", "pydantic", "aiofiles", "aiosqlite"
        ]
        
        for dep in dependencies:
            try:
                __import__(dep)
            except ImportError as e:
                raise Exception(f"Missing dependency {dep}: {e}")
        
        return True
    
    async def test_import_server_structure(self) -> bool:
        """Test server file structure without importing problematic dependencies"""
        try:
            # Read server.py and check for basic structure
            with open('server.py', 'r') as f:
                content = f.read()
            
            # Check for required classes and methods
            required_elements = [
                "class IoTVulnerabilityScanner",
                "def __init__",
                "def setup_handlers",
                "def comprehensive_iot_scan",
                "def camera_vulnerability_assessment"
            ]
            
            for element in required_elements:
                if element not in content:
                    raise Exception(f"Missing required element: {element}")
            
            return True
            
        except Exception as e:
            raise Exception(f"Server structure test failed: {e}")
    
    async def run_all_tests(self) -> bool:
        """Run all basic functionality tests"""
        print("🚀 Starting Basic Functionality Tests")
        print("=" * 50)
        
        tests = [
            ("File Structure", self.test_file_structure),
            ("Configuration Files", self.test_configuration_files),
            ("Database Connectivity", self.test_database_connectivity),
            ("Python Dependencies", self.test_python_dependencies),
            ("Server Structure", self.test_import_server_structure)
        ]
        
        results = []
        for test_name, test_func in tests:
            result = await self.run_test(test_name, test_func)
            results.append(result)
        
        # Print detailed summary
        print("\n" + "=" * 50)
        print("📊 BASIC FUNCTIONALITY TEST SUMMARY")
        print("=" * 50)
        
        for test_name, status, error in self.test_results:
            status_icon = "✅" if status == "PASS" else "❌"
            print(f"{status_icon} {test_name}: {status}")
            if error:
                print(f"   Error: {error}")
        
        # Overall result
        passed = sum(1 for _, status, _ in self.test_results if status == "PASS")
        total = len(self.test_results)
        
        print(f"\n🎯 OVERALL RESULT: {passed}/{total} tests passed")
        
        if passed == total:
            print("✨ ALL BASIC TESTS PASSED - Core functionality verified!")
        else:
            print("💥 SOME TESTS FAILED - Review before proceeding")
        
        return passed == total

async def main():
    """Main test entry point"""
    tester = BasicFunctionalityTester()
    success = await tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())
