#!/usr/bin/env python3
"""
CropAI Deployment Validation Script
Checks: CORS config, env vars, API connectivity, model paths, Groq health
Usage: python validate_deployment.py
"""

import os
import sys
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

class Colors:
    OK = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    INFO = '\033[94m'
    RESET = '\033[0m'

def check(name, condition, details=""):
    status = f"{Colors.OK}✅{Colors.RESET}" if condition else f"{Colors.FAIL}❌{Colors.RESET}"
    print(f"{status} {name}")
    if details:
        print(f"  → {details}")
    return condition

print(f"\n{Colors.INFO}🔍 CropAI Production Deployment Validator{Colors.RESET}\n")

# ===== ENV VARS =====
print(f"{Colors.INFO}[1] Environment Variables{Colors.RESET}")

checks = [
    check("FLASK_ENV", os.getenv('FLASK_ENV') == 'production', 
          f"Current: {os.getenv('FLASK_ENV', 'NOT SET')}"),
    check("GROQ_API_KEY", bool(os.getenv('GROQ_API_KEY')), 
          "Set at: https://console.groq.com"),
    check("ALLOWED_ORIGINS", bool(os.getenv('ALLOWED_ORIGINS')), 
          f"Current: {os.getenv('ALLOWED_ORIGINS', 'NOT SET')}"),
    check("FLASK_SECRET_KEY", len(os.getenv('FLASK_SECRET_KEY', '')) >= 16, 
          "Should be 32+ random chars"),
]

# ===== MODEL =====
print(f"\n{Colors.INFO}[2] ML Model{Colors.RESET}")

base_dir = Path(__file__).parent / 'app'
model_path = base_dir / 'ml_training' / 'models' / 'crop_model_best.pkl'
check("Model Path Exists", model_path.exists(), 
      f"Path: {model_path}")
check("Model Size", model_path.exists() and model_path.stat().st_size > 1024, 
      f"Size: {model_path.stat().st_size / 1024:.2f} KB" if model_path.exists() else "N/A")

# ===== GROQ CONNECTIVITY =====
print(f"\n{Colors.INFO}[3] Groq API Health{Colors.RESET}")

groq_key = os.getenv('GROQ_API_KEY')
if groq_key:
    try:
        from groq import Groq
        client = Groq(api_key=groq_key)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        check("Groq Connection", True, "API key valid, connection successful")
    except Exception as e:
        check("Groq Connection", False, f"Error: {str(e)[:80]}")
else:
    check("Groq Connection", False, "GROQ_API_KEY not set")

# ===== CORS VALIDATION =====
print(f"\n{Colors.INFO}[4] CORS Configuration{Colors.RESET}")

allowed_origins = os.getenv('ALLOWED_ORIGINS', '').split(',')
allowed_origins = [o.strip() for o in allowed_origins if o.strip()]

print(f"  Allowed Origins ({len(allowed_origins)}):")
for origin in allowed_origins:
    print(f"    • {origin}")

check("CORS Setup", len(allowed_origins) > 0, 
      f"{len(allowed_origins)} origin(s) configured")

# ===== LOCAL API TEST (if running locally) =====
if os.getenv('FLASK_ENV') != 'production':
    print(f"\n{Colors.INFO}[5] Local API Test{Colors.RESET}")
    
    test_url = "http://localhost:5000/health"
    try:
        response = requests.get(test_url, timeout=3)
        check("Health Endpoint", response.status_code == 200, 
              f"Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        check("Health Endpoint", False, 
              "Backend not running on localhost:5000")
    except Exception as e:
        check("Health Endpoint", False, f"Error: {str(e)[:60]}")

# ===== SUMMARY =====
print(f"\n{Colors.INFO}[✓] Validation Complete{Colors.RESET}")
print("\nNext Steps:")
print("  1. Fix any ❌ issues above")
print("  2. Run: git commit -m 'fix: deployment validation'")
print("  3. Deploy to Render/Vercel")
print("  4. Run: curl https://YOUR-BACKEND-URL/health\n")
