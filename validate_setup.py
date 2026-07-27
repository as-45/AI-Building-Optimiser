#!/usr/bin/env python3
"""
Pre-Run Validation Script for AI Building Optimizer

Checks:
1. EnergyPlus installation
2. RunPod MCP server connectivity
3. GPU/ChromaDB/config files
4. Environment variables
5. All dependencies installed

Run this BEFORE executing runtime_controller.py
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Tuple, List

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def print_header(title):
    print(f"\n{BLUE}{'='*70}")
    print(f" {title}")
    print(f"{'='*70}{RESET}\n")

def check_mark(status: bool) -> str:
    return f"{GREEN}✅{RESET}" if status else f"{RED}❌{RESET}"

def print_result(name: str, status: bool, details: str = ""):
    symbol = check_mark(status)
    print(f"{symbol} {name}")
    if details:
        print(f"   {YELLOW}→ {details}{RESET}")

def check_energyplus() -> Tuple[bool, str]:
    """Check if EnergyPlus API is available."""
    try:
        from pyenergyplus.api import EnergyPlusAPI
        api = EnergyPlusAPI()
        return True, "EnergyPlus V26.1+ available"
    except ImportError:
        return False, "EnergyPlus API not found. Install: https://energyplus.net/"
    except Exception as e:
        return False, f"EnergyPlus error: {str(e)}"

def check_python_dependencies() -> Tuple[bool, List[str]]:
    """Check if all required Python packages are installed."""
    required = [
        "torch",
        "transformers",
        "chromadb",
        "mcp",
        "fastmcp",
        "requests",
        "numpy",
        "pandas",
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return len(missing) == 0, missing

def check_mcp_server() -> Tuple[bool, str]:
    """Check if MCP server is running on RunPod."""
    mcp_url = os.getenv("MCP_SERVER_URL")
    
    if not mcp_url:
        return False, "MCP_SERVER_URL environment variable not set"
    
    try:
        import requests
        response = requests.get(f"{mcp_url}/health", timeout=5)
        if response.status_code == 200:
            return True, f"MCP Server OK at {mcp_url}"
        else:
            return False, f"MCP Server returned {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, f"Cannot reach {mcp_url} (RunPod not running?)"
    except Exception as e:
        return False, f"MCP server error: {str(e)}"

def check_gpu() -> Tuple[bool, str]:
    """Check if CUDA GPU is available locally (optional, MCP has GPU)."""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            return True, f"GPU available: {gpu_name} (for local inference)"
        else:
            return True, "GPU not available locally (OK - MCP on RunPod has GPU)"
    except Exception as e:
        return False, f"GPU check error: {str(e)}"

def check_chromadb() -> Tuple[bool, str]:
    """Check ChromaDB database."""
    try:
        from memory.chroma_manager import ChromaManager
        cm = ChromaManager()
        collection = cm.get_collection()
        count = collection.count()
        return True, f"ChromaDB OK ({count} episodes stored)"
    except Exception as e:
        return False, f"ChromaDB error: {str(e)}"

def check_config_files() -> Tuple[bool, List[str]]:
    """Check if all required config files exist."""
    required_files = [
        "config/runtime_config.json",
        "config/building_config.json",
        "config/comfort_config.json",
        "config/optimization_config.json",
    ]
    
    optional_files = [
        "model/medium_office.idf",
        "weather/IND_Bangalore.432950_ISHRAE.epw",
    ]
    
    missing = []
    for file in required_files:
        if not (PROJECT_ROOT / file).exists():
            missing.append(f"[CRITICAL] {file}")
    
    for file in optional_files:
        if not (PROJECT_ROOT / file).exists():
            missing.append(f"[WARNING] {file}")
    
    return len([m for m in missing if "CRITICAL" in m]) == 0, missing

def check_runtime_config() -> Tuple[bool, str]:
    """Check runtime configuration."""
    try:
        with open(PROJECT_ROOT / "config/runtime_config.json") as f:
            config = json.load(f)
        
        enable_llm = config.get("enable_llm_control", False)
        enable_memory = config.get("enable_memory_retrieval", False)
        
        if not enable_llm:
            return False, "LLM control is DISABLED. Set 'enable_llm_control': true"
        
        if enable_memory:
            status = "✅ LLM enabled + Memory retrieval enabled (optimal)"
        else:
            status = "⚠️ LLM enabled but memory disabled (suboptimal)"
        
        return True, status
    except Exception as e:
        return False, f"Config parse error: {str(e)}"

def check_output_directory() -> Tuple[bool, str]:
    """Check if output directory exists and is writable."""
    output_dir = PROJECT_ROOT / "outputs" / "runtime"
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        test_file = output_dir / ".write_test"
        test_file.write_text("test")
        test_file.unlink()
        return True, f"Output directory writable: {output_dir}"
    except Exception as e:
        return False, f"Cannot write to output directory: {str(e)}"

def check_mcp_server_url() -> Tuple[bool, str]:
    """Check if MCP_SERVER_URL is set."""
    mcp_url = os.getenv("MCP_SERVER_URL")
    if mcp_url:
        return True, f"MCP_SERVER_URL = {mcp_url}"
    else:
        return False, "MCP_SERVER_URL not set. Set it:\n   " \
               "$env:MCP_SERVER_URL = 'https://your-runpod-url:8000'"

def main():
    """Run all checks."""
    print_header("🔍 AI Building Optimizer - Pre-Run Validation")
    
    checks = [
        ("Environment Variables", [
            ("MCP_SERVER_URL set", check_mcp_server_url),
        ]),
        ("Python Environment", [
            ("EnergyPlus API", check_energyplus),
            ("Python Dependencies", lambda: (len(check_python_dependencies()[1]) == 0, 
                                            ", ".join(check_python_dependencies()[1]) or "All installed")),
            ("GPU Status", check_gpu),
        ]),
        ("Infrastructure", [
            ("MCP Server Connectivity", check_mcp_server),
            ("ChromaDB Database", check_chromadb),
        ]),
        ("Configuration", [
            ("Config Files", check_config_files),
            ("Runtime Config", check_runtime_config),
            ("Output Directory", check_output_directory),
        ]),
    ]
    
    overall_status = True
    
    for category, category_checks in checks:
        print(f"{BLUE}{category}{RESET}")
        print("-" * 70)
        
        for check_name, check_func in category_checks:
            result, details = check_func()
            print_result(check_name, result, details)
            
            if not result and "CRITICAL" in str(details):
                overall_status = False
        
        print()
    
    # Summary
    print_header("📊 Validation Summary")
    
    if overall_status:
        print(f"{GREEN}✅ ALL CRITICAL CHECKS PASSED!{RESET}\n")
        print(f"You can now run:")
        print(f"  {YELLOW}python -m simulation.runtime_controller{RESET}\n")
        return 0
    else:
        print(f"{RED}❌ SOME CRITICAL CHECKS FAILED{RESET}\n")
        print(f"Please fix the issues above before running.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
