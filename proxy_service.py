import subprocess
import os
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET'])
def proxy(path):
    target_url = f"https://{path}" if path else "https://api.ipify.org"
    
    cmd = [
        "curl", "-s", "-x", "http://sazz16014w96:t3vz152mql23@resi.fusionproxy.net:13822",
        "-L", target_url
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    return Response(result.stdout, status=200, content_type='text/plain')
