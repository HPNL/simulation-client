from fastapi import APIRouter

from app.k8s_client import get_k8s_client

router = APIRouter(prefix="/api/v1/containers", tags=["Containers"])


@router.get("/{namespace}/{pod_name}")
def list_containers(namespace: str, pod_name: str):
    k8s = get_k8s_client()
    pod = k8s.read_namespaced_pod(name=pod_name, namespace=namespace)
    return [container.name for container in pod.spec.containers]


@router.get("/{namespace}/{pod_name}/{container_name}")
def get_container_logs(namespace: str, pod_name: str, container_name: str):
    k8s = get_k8s_client()
    logs = k8s.read_namespaced_pod_log(name=pod_name, namespace=namespace, container=container_name)
    return {"logs": logs}


@router.post("/{namespace}/{pod_name}/{container_name}/start")
def start_container(namespace: str, pod_name: str, container_name: str):
    # Kubernetes doesn't allow starting/stopping individual containers directly.
    return {"message": "Start container is not supported directly by Kubernetes"}


@router.post("/{namespace}/{pod_name}/{container_name}/stop")
def stop_container(namespace: str, pod_name: str, container_name: str):
    return {"message": "Stop container is not supported directly by Kubernetes"}


@router.post("/{namespace}/{pod_name}/new")
def create_new_container(namespace: str, pod_name: str, container_manifest: dict):
    return {"message": "Container creation is not supported directly by Kubernetes. Use pod management."}
