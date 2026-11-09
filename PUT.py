import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

datos = {
    "id": 1,
    "title": "Farmacia actualizada",
    "body": "Nueva información de la farmacia",
    "userId": 1
}

try:
    print("Actualizando información...")

    respuesta = requests.put(
        url,
        json=datos,
        timeout=10
    )

    respuesta.raise_for_status()

    print("Recurso actualizado correctamente:")
    print(respuesta.json())

except requests.exceptions.Timeout:
    print("Error: tiempo de espera agotado.")

except requests.exceptions.RequestException as error:
    print("Error en la solicitud:", error)
