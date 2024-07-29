from kubernetes import client

class Namespace:
    def __init__(self):
        self.v1 = client.CoreV1Api()

    def list_namespaces(self):
        namespaces = self.v1.list_namespace()
        namespace_details = []
        for ns in namespaces.items:
            namespace_details.append({
                'name': ns.metadata.name
            })
        return namespace_details
