import json
import requests
from datetime import datetime
from utils.monitor import check_service
from database.database import *

def load_services():
    try:
        with open("services.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Archivo de servicios no encontrado")
        return []
    except Exception as error:
        print(f"Error cargando servicios: {error}")
        return []
    
def save_log(log):
    try:
        with open("logs.json", "r") as file:
            logs = json.load(file)
    except FileNotFoundError:
        logs = []

    logs.append(log)

    with open("logs.json", "w") as file:
        json.dump(logs, file, indent=4)
    
def enviar_a_n8n(url,data):
    try:
        response = requests.post(url, json=data)
        print("Enviado a n8n: ", response.status_code)
    except Exception as e:
        print("Error enviando a n8n: ",e)

def main():
    create_database()
    services = load_services()

    for service in services:
        result = check_service(service["url"])
        log = {
            "service": service["name"],
            "url": service["url"],
            "status": result["status"],
            "date": datetime.now().strftime("%y-%m-%d %H:%M:%S")
        }
        if "code" in result:
            log["code"] = result["code"]
        if "message" in result:
            log["message"] = result["message"]
        save_log(log)
        guardar_en_database(log)
        enviar_a_n8n("http://localhost:5678/webhook-test/monitor-alert",log)

        print(f"\nServicio: {service['name']}")
        print(f"URL: {service['url']}")
        print(f"Estado: {result['status']}")

        if "code" in result:
            print(f"Codigo HTTP: {result['code']}")
        if "message" in result:
            print(f"Error: {result['message']}")

if __name__ == "__main__":
    main()