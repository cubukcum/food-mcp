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
        headers = {"accept": "*/*"}
        # API gereksinimlerinize göre bunu ayarlamanız gerekebilir
        # Bazı API'ler istek gövdesinde veya başlıklarında kimlik bilgileri gerektirir
        response = requests.post(JWT_TOKEN_URL, headers=headers, data='',verify=False)
        response.raise_for_status()
        
        # API doğrudan JWT token string'ini döndürüyor (JSON değil)
        # Content-Type text/plain olduğu için response.text kullanıyoruz
        token = response.text.strip()
        
        # Token'ın geçerli bir JWT formatında olduğunu kontrol et
        if token and len(token.split('.')) == 3:
            return token
        else:
            print(f"Geçersiz JWT token formatı: {token[:50]}...")
            return None
        
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
        
        response = requests.get(MENU_API_URL, headers=headers, verify=False)
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
