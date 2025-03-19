# Pinterest Scraper API

Uma API simples e eficiente para buscar imagens do Pinterest em alta resolução.

## 🚀 Funcionalidades

- Busca de imagens do Pinterest por termo
- Retorno de imagens em alta resolução
- Cache de 30 minutos para otimizar requisições
- Suporte a CORS para integração com qualquer frontend
- Endpoints de monitoramento e saúde da API
- Limpeza manual de cache

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- Flask
- Selenium
- BeautifulSoup4
- Flask-Caching
- Flask-CORS

## 📋 Pré-requisitos

- Python 3.x
- Chrome/Chromium instalado
- ChromeDriver compatível com sua versão do Chrome

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/crynew/pinterest-scraper-api.git
cd pinterest-scraper-api
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a API:
```bash
python pins/main.py
```

## 📡 Endpoints

### Busca de Imagens
```
GET /search/<termo>/<quantidade>
```
Exemplo: `/search/cachorro/5`

### Página Inicial
```
GET /
```
Retorna informações sobre a API e endpoints disponíveis.

### Verificar Saúde
```
GET /health
```
Retorna o status da API e informações do cache.

### Limpar Cache
```
GET /clear-cache
```
Limpa o cache manualmente.

## 💻 Exemplo de Uso

### Com cURL
```bash
curl http://localhost:5000/search/cachorro/5
```

### Com JavaScript
```javascript
fetch('http://localhost:5000/search/cachorro/5')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Com Python
```python
import requests
response = requests.get('http://localhost:5000/search/cachorro/5')
print(response.json())
```

## 📦 Resposta da API

```json
{
    "query": "cachorro",
    "quantidade": 5,
    "resultados": [
        "https://i.pinimg.com/originals/...",
        "https://i.pinimg.com/originals/...",
        ...
    ]
}
```

## 🔒 Segurança

- CORS habilitado para todas as origens
- Cache para reduzir requisições ao Pinterest
- Tratamento de erros robusto

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Suporte

Se você encontrar algum problema ou tiver sugestões, abra uma issue no GitHub.
