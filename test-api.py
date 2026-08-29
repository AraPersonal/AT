import urllib.request
import urllib.error
import json
import os
import sys

# Get API key from somewhere or we can just print the JSON
API_KEY = os.popen("grep 'API_KEY' app/.env | cut -d'=' -f2").read().strip()
if not API_KEY:
    print("No API key")
    sys.exit(0)

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

data = {
    "contents": [
        {"role": "user", "parts": [{"text": "What is 5+5? Use the calculator tool."}]}
    ],
    "tools": [
        {"function_declarations": [{"name": "calculator", "description": "calculator", "parameters": {"type": "OBJECT", "properties": {"expression": {"type": "STRING"}}}}] }
    ]
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode())
        print(json.dumps(res, indent=2))
except urllib.error.HTTPError as e:
    print(f"Error: {e.code} {e.read().decode()}")

