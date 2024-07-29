from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

class KubernetesManager:
    def __init__(self):
        self.provider = None

    def set_provider(self, provider):
        self.provider = provider

    def load_config(self, config_dict):
        try:
            config.load_kube_config_from_dict(config_dict)
        except Exception as e:
            raise Exception(f"Failed to load kubeconfig: {str(e)}")

    def get_resources(self):
        try:
            resources = {
                "pods": self.list_pods(),
                "namespaces": self.list_namespaces(),
                "deployments": self.list_deployments(),
                "services": self.list_services(),
                "ingresses": self.list_ingresses(),
            }
            return resources
        except ApiException as e:
            raise Exception(f"API Error: {e.reason}")

    def list_pods(self):
        v1 = client.CoreV1Api()
        pods = v1.list_pod_for_all_namespaces(watch=False)
        return [pod.metadata.name for pod in pods.items]

    def list_namespaces(self):
        v1 = client.CoreV1Api()
        namespaces = v1.list_namespace()
        return [ns.metadata.name for ns in namespaces.items]

    def list_deployments(self):
        apps_v1 = client.AppsV1Api()
        deployments = apps_v1.list_deployment_for_all_namespaces()
        return [dep.metadata.name for dep in deployments.items]

    def list_services(self):
        v1 = client.CoreV1Api()
        services = v1.list_service_for_all_namespaces()
        return [svc.metadata.name for svc in services.items]

    def list_ingresses(self):
        networking_v1 = client.NetworkingV1Api()
        ingresses = networking_v1.list_ingress_for_all_namespaces()
        return [ing.metadata.name for ing in ingresses.items]
