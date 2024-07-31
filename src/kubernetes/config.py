from kubernetes import client
from datetime import datetime
import yaml

class Config:
    def __init__(self):
        self.v1 = client.CoreV1Api()

    def list_configmaps(self):
        configmaps = self.v1.list_config_map_for_all_namespaces()
        configmap_details = []
        for cm in configmaps.items:
            age = (datetime.utcnow() - cm.metadata.creation_timestamp.replace(tzinfo=None)).days
            configmap_details.append({
                'name': cm.metadata.name,
                'namespace': cm.metadata.namespace,
                'age': f"{age}d"
            })
        return configmap_details

    def get_configmap_yaml(self, namespace, name):
        configmap = self.v1.read_namespaced_config_map(name, namespace, _preload_content=False)
        return configmap.data.decode('utf-8')

    def update_configmap_yaml(self, namespace, name, yaml_content):
        yaml_dict = yaml.safe_load(yaml_content)
        yaml_dict['api_version'] = yaml_dict.pop('apiVersion', None)
        yaml_dict['kind'] = yaml_dict.pop('kind', None)
        configmap_body = client.V1ConfigMap(**yaml_dict)
        self.v1.replace_namespaced_config_map(name, namespace, body=configmap_body)

    def list_secrets(self):
        secrets = self.v1.list_secret_for_all_namespaces()
        secret_details = []
        for secret in secrets.items:
            age = (datetime.utcnow() - secret.metadata.creation_timestamp.replace(tzinfo=None)).days
            secret_details.append({
                'name': secret.metadata.name,
                'namespace': secret.metadata.namespace,
                'type': secret.type,
                'age': f"{age}d"
            })
        return secret_details

    def get_secret_yaml(self, namespace, name):
        secret = self.v1.read_namespaced_secret(name, namespace, _preload_content=False)
        return secret.data.decode('utf-8')

    def update_secret_yaml(self, namespace, name, yaml_content):
        yaml_dict = yaml.safe_load(yaml_content)
        yaml_dict['api_version'] = yaml_dict.pop('apiVersion', None)
        yaml_dict['kind'] = yaml_dict.pop('kind', None)
        secret_body = client.V1Secret(**yaml_dict)
        self.v1.replace_namespaced_secret(name, namespace, body=secret_body)
