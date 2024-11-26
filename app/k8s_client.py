from kubernetes import client, config

def get_k8s_client():
    try:
        # Load kubeconfig for local development
        config.load_kube_config()
    except:
        # Load in-cluster config if running inside Kubernetes
        config.load_incluster_config()
    return client.CoreV1Api()
