from kubernetes import client, config

config.load_kube_config()

def get_user_service(user_id):
    v1 = client.CoreV1Api()
    services = v1.list_service_for_all_namespaces()
    for svc in services.items:
        if svc.metadata.labels and svc.metadata.labels.get("user") == user_id:
            return svc.metadata.name
    return None

user_id = "user1"
service_name = get_user_service(user_id)
if service_name:
    print(f"Service for user {user_id} is {service_name}")
else:
    print(f"No service found for user {user_id}")
