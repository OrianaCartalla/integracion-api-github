import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

try:
    print("Eliminando recurso...")

    respuesta = requests.delete(
        url,
        timeout=10
    )

    respuesta.raise_for_status()

    print("Recurso eliminado correctamente.")
    print("Código HTTP:", respuesta.status_code)

except requests.exceptions.Timeout:
    print("Error: tiempo de espera agotado.")

except requests.exceptions.RequestException as error:
    print("Error en la solicitud:", error)
