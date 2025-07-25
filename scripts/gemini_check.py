#!/usr/bin/env python3
import os
import subprocess
import sys
import requests
import json

def check_with_gemini(content, filename):
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("│ [WARN] GEMINI_API_KEY not set, skipping AI check")
        return "PASS"

    prompt = f"""
Review this code for issues. Look for:
1.  Potential bugs (e.g., off-by-one errors, null pointer issues).
2.  Typos in comments or strings (e.g., 'length', 'recieve').
3.  `console.log` or other debugging statements.
4.  Incomplete features (e.g., `TODO` without a ticket).
5.  Areas for improvement or refactoring.

File: {filename}
Content:
{content}

Return a concise review. If no issues, return only 'PASS'. Otherwise, return 'FAIL:' followed by a bulleted list of issues.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    if os.environ.get('GEMINI_CHECK_DEBUG') == 'true':
        print(f"\nSending to Gemini API:\n{json.dumps(payload, indent=2)}\n")

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()

        if os.environ.get('GEMINI_CHECK_DEBUG') == 'true':
            print(f"\nReceived from Gemini API:\n{json.dumps(result, indent=2)}\n")

        if 'candidates' not in result:
            print(f"Gemini API error: 'candidates' key not in response. Full response: {result}")
            return "FAIL: API Error"
        return result['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.HTTPError as e:
        print(f"Gemini API HTTP error: {e}")
        print(f"Response: {e.response.text}")
        return "FAIL: API Error"
    except Exception as e:
        print(f"Gemini API error: {e}")
        return "FAIL: API Error"

def main():
    print("┌───────────────────────────────────────────┐")
    print("│ Running Gemini AI Pre-Commit Code Review  │")
    print("└───────────────────────────────────────────┘")
    
    # Get staged files
    try:
        staged_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only'], 
                                             encoding='utf-8').strip().split('\n')
        staged_files = [f for f in staged_files if f and f.endswith(('.js', '.py', '.ts', '.md')) and not f.startswith('scripts/') and f != 'README.md']
    except:
        print("│ [INFO] No files to check.")
        print("└───────────────────────────────────────────┘")
        return 0

    if not staged_files:
        print("│ [INFO] No relevant files to check.")
        print("└───────────────────────────────────────────┘")
        return 0
    
    has_errors = False
    
    for file in staged_files:
        if not os.path.exists(file):
            continue
            
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        if len(content) > 8000:  # Skip large files
            print(f"│ [SKIP] {file} (file too large)")
            continue

        print(f"│ [....] Checking {file}")
        result = check_with_gemini(content, file)

        if result.startswith('FAIL'):
            print(f"│ [FAIL] {file}")
            # Indent the reason for failure
            for line in result.split('\n'):
                print(f"│        {line}")
            has_errors = True
        else:
            print(f"│ [ OK ] {file}")
    
    print("├───────────────────────────────────────────┤")
    if has_errors:
        print("│ [FAIL] Commit rejected. Please fix the issues above.")
        print("└───────────────────────────────────────────┘")
        return 1

    print("│ [PASS] All checks passed. Commit approved.")
    print("└───────────────────────────────────────────┘")
    return 0

if __name__ == "__main__":
    sys.exit(main())