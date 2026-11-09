
import os
import re
import json
import requests

API_URL = "https://api.github.com/users/{usuario}/repos"
ARCHIVO_SALIDA = "repositorios.json"
TIMEOUT = 10
REPOS_POR_PAGINA = 100


def validar_usuario(usuario):
    """Comprueba que el nombre de usuario tenga un formato permitido."""

    if not usuario or len(usuario) > 39:
        return False

    if not re.fullmatch(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*", usuario):
        return False

    if usuario.startswith("-") or usuario.endswith("-"):
        return False

    return True


def obtener_repositorios(usuario):
    """Obtiene todos los repositorios públicos mediante paginación."""

    url = API_URL.format(usuario=usuario)
    token = os.getenv("GITHUB_TOKEN")

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # El token es opcional y nunca se escribe directamente en el código.
    if token:
        headers["Authorization"] = f"Bearer {token}"

    repositorios = []
    pagina = 1

    with requests.Session() as sesion:
        while True:
            parametros = {
                "per_page": REPOS_POR_PAGINA,
                "page": pagina
            }

            respuesta = sesion.get(
                url,
                headers=headers,
                params=parametros,
                timeout=TIMEOUT
            )

            respuesta.raise_for_status()

            datos = respuesta.json()

            if not isinstance(datos, list):
                raise ValueError(
                    "La API no devolvió una lista de repositorios."
                )

            repositorios.extend(datos)

            if len(datos) < REPOS_POR_PAGINA:
                break

            pagina += 1

    return repositorios


def guardar_resultado(repositorios, archivo):
    """Guarda el resumen de repositorios en un archivo JSON."""

    resumen = []

    for repo in repositorios:
        resumen.append({
            "nombre": repo.get("name"),
            "lenguaje": repo.get("language"),
            "estrellas": repo.get("stargazers_count")
        })

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(resumen, f, indent=4, ensure_ascii=False)


def main():
    usuario = input("Ingrese usuario de GitHub: ").strip()

    if not validar_usuario(usuario):
        print("Nombre de usuario inválido. Revise el formato e intente nuevamente.")
        return

    try:
        repositorios = obtener_repositorios(usuario)

        for repo in repositorios:
            print(
                repo.get("name"),
                "-",
                repo.get("stargazers_count"),
                "estrellas"
            )

        guardar_resultado(repositorios, ARCHIVO_SALIDA)

        print(f"Archivo {ARCHIVO_SALIDA} generado correctamente.")

    except requests.exceptions.Timeout:
        print("Error: la solicitud superó el tiempo de espera.")

    except requests.exceptions.HTTPError as error:
        estado = (
            error.response.status_code
            if error.response is not None
            else "desconocido"
        )

        if estado == 404:
            print("Error 404: no se encontró el usuario de GitHub.")

        elif estado == 403:
            print("Error 403: acceso limitado o límite de solicitudes alcanzado.")

        else:
            print(f"GitHub devolvió un error HTTP: {estado}")

    except requests.exceptions.ConnectionError:
        print("Error: no fue posible establecer conexión con GitHub.")

    except requests.exceptions.RequestException as error:
        print(f"Error durante la solicitud a GitHub: {error}")

    except ValueError as error:
        print(f"Error al interpretar la respuesta de GitHub: {error}")

    except OSError as error:
        print(f"Error al guardar el archivo: {error}")

    else:
        print("Proceso terminado.")


if __name__ == "__main__":
    main()
