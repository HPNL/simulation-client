from fastapi import APIRouter
from kubernetes import client

from app.k8s_client import get_k8s_client

router = APIRouter(prefix="/api/v1/namespaces", tags=["Namespaces"])


@router.get("/")
def list_namespaces():
    k8s = get_k8s_client()
    namespaces = k8s.list_namespace()
    return [ns.metadata.name for ns in namespaces.items]


@router.post("/")
def create_namespace(name: str):
    k8s = get_k8s_client()
    namespace = client.V1Namespace(metadata=client.V1ObjectMeta(name=name))
    k8s.create_namespace(namespace)
    return {"message": f"Namespace {name} created"}


@router.delete("/{name}")
def delete_namespace(name: str):
    k8s = get_k8s_client()
    k8s.delete_namespace(name)
    return {"message": f"Namespace {name} deleted"}


@router.get("/{name}")
def get_namespace_details(name: str):
    k8s = get_k8s_client()
    namespace = k8s.read_namespace(name)
    return {"name": namespace.metadata.name, "status": namespace.status.phase}
