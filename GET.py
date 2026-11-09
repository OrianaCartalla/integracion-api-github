
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

try:
    print("Consultando información de la API...")

    respuesta = requests.get(url, timeout=10)
    respuesta.raise_for_status()

    datos = respuesta.json()

    print("Información obtenida correctamente:")
    print(datos)

except requests.exceptions.Timeout:
    print("Error: tiempo de espera agotado.")

except requests.exceptions.RequestException as error:
    print("Error en la solicitud:", error)
