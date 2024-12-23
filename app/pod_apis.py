from fastapi import APIRouter
from kubernetes import client

from app.k8s_client import get_k8s_client

router = APIRouter(prefix="/pods", tags=["Pods"])


@router.get("/{namespace}")
def list_pods(namespace: str):
    k8s = get_k8s_client()
    pods = k8s.list_namespaced_pod(namespace=namespace)
    return [pod.metadata.name for pod in pods.items]


@router.get("/{namespace}/{name}")
def get_pod_details(namespace: str, name: str):
    k8s = get_k8s_client()
    pod = k8s.read_namespaced_pod(name=name, namespace=namespace)
    return {"name": pod.metadata.name, "status": pod.status.phase}


@router.post("/{namespace}")
def create_pod(namespace: str, pod_manifest: dict):
    k8s = get_k8s_client()
    pod = client.V1Pod(**pod_manifest)
    k8s.create_namespaced_pod(namespace=namespace, body=pod)
    return {"message": "Pod created"}


@router.delete("/{namespace}/{name}")
def delete_pod(namespace: str, name: str):
    k8s = get_k8s_client()
    k8s.delete_namespaced_pod(name=name, namespace=namespace)
    return {"message": f"Pod {name} deleted"}
