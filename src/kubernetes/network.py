from kubernetes import client

class Network:
    def __init__(self):
        self.v1 = client.CoreV1Api()
        self.networking_v1 = client.NetworkingV1Api()

    def list_services(self):
        services = self.v1.list_service_for_all_namespaces()
        service_details = []
        for svc in services.items:
            service_details.append({
                'name': svc.metadata.name,
                'namespace': svc.metadata.namespace
            })
        return service_details

    def list_ingresses(self):
        ingresses = self.networking_v1.list_ingress_for_all_namespaces()
        ingress_details = []
        for ing in ingresses.items:
            ingress_details.append({
                'name': ing.metadata.name,
                'namespace': ing.metadata.namespace
            })
        return ingress_details
