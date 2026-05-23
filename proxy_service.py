from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

PROXY = "http://sazz16014w96:t3vz152mql23@resi.fusionproxy.net:13822"
proxies = {"http": PROXY, "https": PROXY}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    target_url = f"https://{path}" if path else "https://api.ipify.org"
    
    resp = requests.request(
        method=request.method,
        url=target_url,
        headers={k: v for k, v in request.headers if k != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        proxies=proxies,
        allow_redirects=False
    )
    
    response = Response(resp.content, status=resp.status_code)
    for k, v in resp.headers.items():
        response.headers[k] = v
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
