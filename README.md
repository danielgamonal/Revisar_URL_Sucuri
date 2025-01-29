Análisis de Seguridad y Contenido Web con Sucuri API

Descripción

Este script en Python 3.12 permite analizar múltiples sitios web utilizando la API de Sucuri y verificar si contienen el texto de marcador de posición "lorem ipsum" en su contenido. Genera un informe en formato Excel con los siguientes datos:

Estado del certificado SSL (emisor y fecha de expiración).

Tipo de servidor en el que corre el sitio.

Redirecciones activas.

Versión del CMS detectado (si aplica).

Rating de seguridad del sitio según Sucuri.

Fecha del último escaneo de seguridad.

Presencia del texto "lorem ipsum" en la página.

Requisitos

Este script requiere Python 3.12 y las siguientes librerías:

pip install requests pandas openpyxl

Uso

Crear un archivo urls.txt con una lista de URLs (una por línea).

Ejecutar el script:

python script.py

Se generará un archivo resultados_sucuri.xlsx con los datos analizados.

Notas

La API de Sucuri no requiere autenticación para escaneos básicos.

Si una URL no responde o presenta errores, los datos se registrarán como "Error" en el Excel.

La detección de "lorem ipsum" es sensible a minúsculas y puede verse afectada por técnicas de ofuscación en algunas páginas.
