import requests
import pandas as pd

def obtener_datos_sucuri(url):
    api_url = f"https://sitecheck.sucuri.net/api/v3/?scan={url}"
    try:
        print(f"Consultando API para {url}...")
        response = requests.get(api_url)
        response.raise_for_status()  # Lanza una excepción para códigos de estado HTTP de error
        print(f"Respuesta recibida para {url}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar la API de Sucuri para {url}: {e}")
        return None

def buscar_lorem_ipsum(url):
    try:
        print(f"Revisando contenido de la página {url} para 'lorem ipsum'...")
        response = requests.get(url, timeout=10)  # Ajusta el timeout según sea necesario
        response.raise_for_status()
        # Verificar si "lorem ipsum" está en el contenido de la página
        if "lorem ipsum" in response.text.lower():
            print(f"'lorem ipsum' encontrado en {url}")
            return "Sí"
        else:
            return "No"
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder al contenido de {url}: {e}")
        return "Error"

def procesar_urls_desde_txt(ruta_archivo_txt, ruta_archivo_excel):
    # Leer URLs desde el archivo TXT
    try:
        with open(ruta_archivo_txt, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
        print(f"Se han leído {len(urls)} URLs del archivo {ruta_archivo_txt}")
    except FileNotFoundError:
        print(f"El archivo {ruta_archivo_txt} no se encuentra.")
        return

    datos = []
    for url in urls:
        datos_sucuri = obtener_datos_sucuri(url)
        lorem_ipsum = buscar_lorem_ipsum(url)  # Verificar "lorem ipsum" en el contenido
        if datos_sucuri:
            # Obtener la versión de CMS si está disponible, o asignar "N/A" si falta
            cms_info = datos_sucuri.get("software", {}).get("cms", [{}])[0]
            version_cms = cms_info.get("version", "N/A")

            datos.append({
                "URL": url,
                "Certificado": datos_sucuri.get("tls", {}).get("cert_issuer", "N/A"),
                "Expiración Cert.": datos_sucuri.get("tls", {}).get("cert_expires", "N/A"),
                "Servidor": datos_sucuri.get("site", {}).get("running_on", ["N/A"])[0],
                "Redirecciona a": datos_sucuri.get("site", {}).get("redirects_to", ["N/A"])[0],
                "Versión CMS": version_cms,
                "Rating Seguridad": datos_sucuri.get("ratings", {}).get("security", {}).get("rating", "N/A"),
                "Último Escaneo": datos_sucuri.get("scan", {}).get("last_scan", "N/A"),
                "'Lorem Ipsum' encontrado": lorem_ipsum
            })
        else:
            datos.append({
                "URL": url,
                "Certificado": "Error",
                "Expiración Cert.": "Error",
                "Servidor": "Error",
                "Redirecciona a": "Error",
                "Versión CMS": "Error",
                "Rating Seguridad": "Error",
                "Último Escaneo": "Error",
                "'Lorem Ipsum' encontrado": "Error"
            })

    # Crear un DataFrame y guardar en Excel
    print("Guardando datos en el archivo Excel...")
    df = pd.DataFrame(datos)
    df.to_excel(ruta_archivo_excel, index=False)
    print(f"Datos guardados en {ruta_archivo_excel}")

# Configuración de rutas
ruta_archivo_txt = "urls.txt"  # Ruta del archivo TXT
ruta_archivo_excel = "resultados_sucuri.xlsx"  # Ruta del archivo Excel

# Ejecutar el procesamiento
procesar_urls_desde_txt(ruta_archivo_txt, ruta_archivo_excel)
