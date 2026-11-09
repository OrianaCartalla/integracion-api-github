import requests

url = "https://jsonplaceholder.typicode.com/posts"

datos = {
    "title": "Nueva farmacia",
    "body": "Farmacia Central",
    "userId": 1
}

try:
    print("Enviando información a la API...")

    respuesta = requests.post(
        url,
        json=datos,
        timeout=10
    )

    respuesta.raise_for_status()

    print("Recurso creado correctamente:")
    print(respuesta.json())

except requests.exceptions.Timeout:
    print("Error: tiempo de espera agotado.")

except requests.exceptions.RequestException as error:
    print("Error en la solicitud:", error)
