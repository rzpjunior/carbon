import yaml

def generate_yaml_dict(resource_type, field_values):
    if resource_type == 'Ingress':
        return {
            'apiVersion': 'networking.k8s.io/v1',
            'kind': 'Ingress',
            'metadata': {'name': field_values['name'], 'namespace': field_values['namespace']},
            'spec': {'rules': yaml.safe_load(field_values['rules'])}
        }
    elif resource_type == 'Deployment':
        return {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {'name': field_values['name'], 'namespace': field_values['namespace']},
            'spec': {
                'replicas': int(field_values['replicas']),
                'selector': {'matchLabels': {'app': field_values['name']}},
                'template': {
                    'metadata': {'labels': {'app': field_values['name']}},
                    'spec': {'containers': yaml.safe_load(field_values['containers'])}
                }
            }
        }
    elif resource_type == 'Service':
        return {
            'apiVersion': 'v1',
            'kind': 'Service',
            'metadata': {'name': field_values['name'], 'namespace': field_values['namespace']},
            'spec': {'ports': yaml.safe_load(field_values['ports'])}
        }
    elif resource_type == 'Namespace':
        return {
            'apiVersion': 'v1',
            'kind': 'Namespace',
            'metadata': {'name': field_values['name']}
        }
    elif resource_type == 'Secret':
        return {
            'apiVersion': 'v1',
            'kind': 'Secret',
            'metadata': {'name': field_values['name'], 'namespace': field_values['namespace']},
            'data': yaml.safe_load(field_values['data'])
        }
    elif resource_type == 'ConfigMap':
        return {
            'apiVersion': 'v1',
            'kind': 'ConfigMap',
            'metadata': {'name': field_values['name'], 'namespace': field_values['namespace']},
            'data': yaml.safe_load(field_values['data'])
        }
    return {}
