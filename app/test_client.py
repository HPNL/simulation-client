from k8s_client import get_k8s_client

k8s = get_k8s_client()
namespaces = k8s.list_namespace()

for ns in namespaces.items:
    print(ns.metadata.name)
