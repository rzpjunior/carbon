import yaml
from kubernetes import client
from datetime import datetime

class Network:
    def __init__(self):
        self.v1 = client.CoreV1Api()
        self.networking_v1 = client.NetworkingV1Api()

    def list_services(self):
        services = self.v1.list_service_for_all_namespaces()
        service_details = []
        for svc in services.items:
            ports = ', '.join([f"{port.port}:{port.target_port}/{port.protocol}" for port in svc.spec.ports])
            external_ip = ', '.join([ingress.ip for ingress in svc.status.load_balancer.ingress if ingress.ip]) if svc.status.load_balancer.ingress else '-'
            selector = ', '.join([f"{k}={v}" for k, v in svc.spec.selector.items()]) if svc.spec.selector else '-'
            age = (datetime.utcnow() - svc.metadata.creation_timestamp.replace(tzinfo=None)).days
            service_details.append({
                'name': svc.metadata.name,
                'namespace': svc.metadata.namespace,
                'type': svc.spec.type,
                'cluster_ip': svc.spec.cluster_ip,
                'ports': ports,
                'external_ip': external_ip,
                'selector': selector,
                'age': f"{age}d",
                'status': 'Pending' if svc.status.load_balancer.ingress else 'Active'
            })
        return service_details

    def list_ingresses(self):
        ingresses = self.networking_v1.list_ingress_for_all_namespaces()
        ingress_details = []
        for ing in ingresses.items:
            load_balancers = ', '.join([ingress.ip for ingress in (ing.status.load_balancer.ingress or []) if ingress.ip]) or '-'
            rules = ', '.join([f"{rule.host or '-'}{' -> ' + ', '.join([path.path for path in (rule.http.paths or []) if path.path])}" for rule in (ing.spec.rules or []) if rule]) or '-'
            age = (datetime.utcnow() - ing.metadata.creation_timestamp.replace(tzinfo=None)).days
            ingress_details.append({
                'name': ing.metadata.name,
                'namespace': ing.metadata.namespace,
                'load_balancers': load_balancers,
                'rules': rules,
                'age': f"{age}d"
            })
        return ingress_details
    
    def get_ingress_yaml(self, namespace, name):
        ingress = self.networking_v1.read_namespaced_ingress(name, namespace, _preload_content=False)
        return ingress.data.decode('utf-8')

    def update_ingress_yaml(self, namespace, name, yaml_content):
        yaml_dict = yaml.safe_load(yaml_content)
        yaml_dict['api_version'] = yaml_dict.pop('apiVersion', None)
        yaml_dict['kind'] = yaml_dict.pop('kind', None)
        ingress_body = client.V1Ingress(**yaml_dict)
        self.networking_v1.replace_namespaced_ingress(name, namespace, body=ingress_body)

    def get_service_yaml(self, namespace, name):
        service = self.v1.read_namespaced_service(name, namespace, _preload_content=False)
        return service.data.decode('utf-8')

    def update_service_yaml(self, namespace, name, yaml_content):
        yaml_dict = yaml.safe_load(yaml_content)
        yaml_dict['api_version'] = yaml_dict.pop('apiVersion', None)
        yaml_dict['kind'] = yaml_dict.pop('kind', None)
        service_body = client.V1Service(**yaml_dict)
        self.v1.replace_namespaced_service(name, namespace, body=service_body)
