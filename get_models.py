import urllib.request
import json
import os

req = urllib.request.Request("https://api.groq.com/openai/v1/models")
req.add_header("Authorization", f"Bearer {os.environ.get('GROQ_API_KEY')}")
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
        for model in data["data"]:
            if "vision" in model["id"].lower():
                print(model["id"])
except Exception as e:
    print(f"Error: {e}")
