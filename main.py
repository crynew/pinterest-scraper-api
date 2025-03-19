from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask_caching import Cache
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Origin"],
        "supports_credentials": True,
        "max_age": 3600
    }
})

cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 1800  
})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "mensagem": "API Pinterest Scraper está funcionando!",
        "uso": "Use /search/<termo>/<quantidade> para buscar imagens",
        "exemplo": "/search/cachorro/5",
        "endpoints": {
            "/": "Página inicial",
            "/health": "Verificar saúde da API",
            "/clear-cache": "Limpar cache manualmente"
        }
    })

@app.route('/health')
def health_check():
    cache_info = {
        "tipo": cache.config['CACHE_TYPE'],
        "timeout_padrao": cache.config['CACHE_DEFAULT_TIMEOUT'],
        "tempo_atual": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify({
        "status": "healthy",
        "cache": cache_info
    })

@app.route('/clear-cache')
def clear_cache():
    try:
        cache.clear()
        return jsonify({
            "status": "success",
            "mensagem": "Cache limpo com sucesso!",
            "tempo": time.strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "mensagem": f"Erro ao limpar cache: {str(e)}"
        }), 500

def scrape_pinterest(query, quantidade):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)

        url = f"https://www.pinterest.com/search/pins/?q={query}"
        driver.get(url)

        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()  

        pins = soup.find_all('div', {'data-test-id': 'pin'}, limit=int(quantidade))
        resultados = []

        for pin in pins:
            img = pin.find('img')
            if img:
                img_src = img.get('src')
                if img_src:
                    img_src = img_src.replace('236x', 'originals')
                    resultados.append(img_src)

        return resultados if resultados else {"erro": "Nenhum resultado encontrado"}

    except Exception as e:
        return {"erro": str(e)}

@app.route('/search/<query>/<value>')
@cache.memoize(timeout=1800)  
def search_pinterest(query, value):
    try:
        quantidade = int(value)
        if quantidade <= 0:
            return jsonify({"erro": "A quantidade deve ser maior que 0"}), 400

        resultados = scrape_pinterest(query, quantidade)
        return jsonify({
            "query": query,
            "quantidade": quantidade,
            "resultados": resultados
        })

    except ValueError:
        return jsonify({"erro": "Quantidade deve ser um número inteiro"}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
