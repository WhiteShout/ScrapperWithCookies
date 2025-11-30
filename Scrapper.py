import requests
from bs4 import BeautifulSoup
import json
from http.cookiejar import MozillaCookieJar, LoadError
from urllib.parse import urlparse
import os

class WebScraperConCookies:
    def __init__(self, cookies_file=None):
        """
        Inicializa el scraper con una sesión que mantiene cookies automáticamente.
        :param cookies_file: Ruta opcional a un archivo .txt con cookies en formato Netscape/Mozilla
        """
        self.session = requests.Session()
        self.cookies_file = cookies_file or "cookies.txt"
        self.dominio_actual = None

        # Cabeceras realistas para evitar ser bloqueado
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        if os.path.exists(self.cookies_file):
            self.cargar_cookies()
    
    def cargar_cookies(self):
        """Carga cookies desde un archivo en formato Netscape"""
        jar = MozillaCookieJar(self.cookies_file)
        try:
            jar.load(ignore_discard=True, ignore_expires=True)
            for cookie in jar:
                self.session.cookies.set_cookie(cookie)
            print(f"Cookies cargadas desde {self.cookies_file}")
        except LoadError:
            print("Error al cargar las cookies (archivo corrupto o vacío)")
        except FileNotFoundError:
            print(f"Archivo {self.cookies_file} no encontrado")

    def guardar_cookies(self):
        """Guarda las cookies actuales en un archivo para usarlas después"""
        jar = MozillaCookieJar(self.cookies_file)
        for cookie in self.session.cookies:
            jar.set_cookie(cookie)
        jar.save(ignore_discard=True, ignore_expires=True)
        print(f"Cookies guardadas en {self.cookies_file}")

    def agregar_cookies_manual(self, cookies_dict):
        """Agrega cookies manualmente como diccionario"""
        for name, value in cookies_dict.items():
            if self.dominio_actual:
                self.session.cookies.set(name, value, domain=self.dominio_actual)
            else:
                self.session.cookies.set(name, value)
        print("Cookies manuales agregadas")

    def get(self, url, params=None, permitir_redirecciones=True):
        """Realiza una petición GET manteniendo cookies"""
        response = self.session.get(url, params=params, allow_redirects=permitir_redirecciones, timeout=20)
        self.dominio_actual = urlparse(response.url).netloc
        return response
    
    def post(self, url, data=None, json_data=None):  
        """Realiza una petición POST manteniendo cookies"""
        response = self.session.post(url, data=data, json=json_data, timeout=20)
        self.dominio_actual = urlparse(response.url).netloc
        return response


if __name__ == "__main__":
    scraper = WebScraperConCookies(cookies_file="mis_cookies.txt")
    
    print("\n=== Prueba 1: Establecer cookies con GET ===")
    r = scraper.get("https://httpbin.org/cookies/set", params={"mi_cookie": "12345", "sesion_activa": "true"})
    print("Respuesta:", r.status_code)
    
    print("\n=== Prueba 2: Verificar cookies ===")
    r = scraper.get("https://httpbin.org/cookies")
    print("Cookies actuales en la sesión:")
    print(json.dumps(r.json(), indent=2))
    
    print("\n=== Prueba 3: Guardar cookies ===")
    scraper.guardar_cookies()
    
    print("\n=== Prueba 4: Agregar cookies manualmente ===")
    scraper.agregar_cookies_manual({"manual_cookie": "valor123"})
    r = scraper.get("https://httpbin.org/cookies")
    print("Cookies después de agregar manual:")
    print(json.dumps(r.json(), indent=2))

    print("\n=== Prueba 5: Realizar get sin cookies ===")
    r = scraper.get("https://es.python.org/", permitir_redirecciones=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    print("\n=== Titulo de la página ===")
    print("Respuesta:", soup.title.string)
    print("\n=== Contenido de la página ===")
    print(soup.prettify()[:200])
    print("\n=== Busqueda de ultimas noticias ===")
    print("Buscar en la página los divs con clase 'mb-3 col':")
    ultimas_noticias = soup.find_all('div', class_='mb-3 col')
    for noticia in ultimas_noticias:
        #Extraer título clase post-title, y enlace del primer <a> y resumen clase post-content
        titulo = noticia.find(class_='post-title').text
        enlace = noticia.find('a')['href']
        resumen = noticia.find(class_='post-content').text
        print(f"- {titulo}: {enlace}")
        print(f"  Resumen: {resumen}")

