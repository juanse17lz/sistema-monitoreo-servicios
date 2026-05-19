import json
from datetime import datetime
from utils.monitor import check_service

def load_services():
    with open("services.json", "r") as file:
        return json.load(file)
    
def save_log(log):
    with open("logs.json", "r") as file:
        logs = json.load(file)

    logs.append(log)

    with open("logs.json", "w") as file:
        json.dump(logs, file, indent=4)
    
def main():
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

        print(f"\nServicio: {service['name']}")
        print(f"URL: {service['url']}")
        print(f"Estado: {result['status']}")

        if "code" in result:
            print(f"Codigo HTTP: {result['code']}")
        if "message" in result:
            print(f"Error: {result['message']}")

if __name__ == "__main__":
    main()