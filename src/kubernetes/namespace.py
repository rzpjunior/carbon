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

    def delete_namespace(self, name):
        self.v1.delete_namespace(name)

    def get_namespace_yaml(self, name):
        namespace = self.v1.read_namespace(name)
        return client.ApiClient().sanitize_for_serialization(namespace)

    def update_namespace_yaml(self, name, yaml_content):
        body = client.V1Namespace(
            metadata=client.V1ObjectMeta(name=name),
            spec=yaml_content.get('spec')
        )
        self.v1.patch_namespace(name, body)
