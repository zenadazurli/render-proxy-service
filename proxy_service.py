from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

PROXY = "http://sazz16014w96:t3vz152mql23@resi.fusionproxy.net:13822"
proxies = {"http": PROXY, "https": PROXY}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH'])
def proxy(path):
    # Costruisce l'URL di destinazione
    target_url = f"https://{path}" if path else "https://api.ipify.org"
    
    # Prepara gli header da inoltrare (esclude Host e altri header specifici di Flask)
    headers = {}
    for key, value in request.headers:
        if key.lower() not in ['host', 'content-length']:
            headers[key] = value
    
    try:
        # Inoltra la richiesta a FusionProxy
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            proxies=proxies,
            allow_redirects=False,
            timeout=30
        )
        
        # Costruisce la risposta
        response = Response(resp.content, status=resp.status_code)
        for key, value in resp.headers.items():
            if key.lower() not in ['content-encoding', 'content-length', 'transfer-encoding']:
                response.headers[key] = value
        
        return response
        
    except requests.exceptions.RequestException as e:
        return Response(f"Proxy error: {str(e)}", status=502)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
