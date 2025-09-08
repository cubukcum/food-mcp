from mcp.server.fastmcp import FastMCP
import requests
import os
import json

# Ortam değişkenlerinden yapılandırma al
MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
MCP_PORT = int(os.getenv("MCP_PORT", "8001"))
JWT_TOKEN_URL = os.getenv("JWT_TOKEN_URL", "http://localhost:5000/auth/token")
MENU_API_URL = os.getenv("MENU_API_URL", "http://localhost:5000/api/menu")

# MCP sunucusu oluştur
mcp = FastMCP("Menu MCP", host=MCP_HOST, port=MCP_PORT)

def jwt_token_al():
    """
    Kimlik doğrulama endpoint'inden JWT token al.
    Başarılı olursa token string'ini, başarısız olursa None döndürür.
    """
    try:
        # API gereksinimlerinize göre bunu ayarlamanız gerekebilir
        # Bazı API'ler istek gövdesinde veya başlıklarında kimlik bilgileri gerektirir
        response = requests.post(JWT_TOKEN_URL)
        response.raise_for_status()
        
        # Yanıtın 'token' alanı içerdiğini varsayıyoruz
        # API'nizin yanıt formatına göre bunu ayarlayın
        token_data = response.json()
        return token_data.get('token') or token_data.get('access_token')
        
    except requests.exceptions.RequestException as e:
        print(f"JWT token alınırken hata: {e}")
        return None

def token_ile_menu_al(token):
    """
    JWT token kullanarak menüyü al.
    Başarılı olursa menü verilerini, başarısız olursa None döndürür.
    """
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(MENU_API_URL, headers=headers)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Token ile menü alınırken hata: {e}")
        return None

@mcp.tool()
def menu_al():
    """
    JWT kimlik doğrulama kullanarak restoran menüsünü getir.
    Önce JWT token alır, sonra menüyü getirmek için kullanır.
    """
    # Adım 1: JWT token al
    token = jwt_token_al()
    if not token:
        return {"error": "JWT token alınamadı"}
    
    # Adım 2: Token kullanarak menüyü al
    menu_data = token_ile_menu_al(token)
    if menu_data is None:
        return {"error": "JWT token ile menü getirilemedi"}
    
    return menu_data

if __name__ == "__main__":
    print(f"Menü MCP {MCP_HOST}:{MCP_PORT} adresinde çalışıyor")
    mcp.run(transport="streamable-http")
