import yaml

def generate_yaml_dict(resource_type, field_values):
    if resource_type == 'Ingress':
        return {
            'apiVersion': 'networking.k8s.io/v1',
            'kind': 'Ingress',
            'metadata': {
                'name': field_values['name'],
                'namespace': field_values['namespace'],
                'annotations': yaml.safe_load(field_values['annotations'])
            },
            'spec': {
                'ingressClassName': field_values['ingress_class_name'],
                'rules': [{
                    'host': field_values['host'],
                    'http': {
                        'paths': [{
                            'path': field_values['path'],
                            'pathType': 'Prefix',
                            'backend': {
                                'service': {
                                    'name': field_values['service_name'],
                                    'port': {
                                        'number': int(field_values['service_port'])
                                    }
                                }
                            }
                        }]
                    }
                }]
            }
        }
    elif resource_type == 'Deployment':
        return {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {
                'name': field_values['name'],
                'namespace': field_values['namespace'],
                'labels': yaml.safe_load(field_values['labels'])
            },
            'spec': {
                'replicas': int(field_values['replicas']),
                'selector': {
                    'matchLabels': {'app': field_values['name']}
                },
                'template': {
                    'metadata': {
                        'labels': {'app': field_values['name']}
                    },
                    'spec': {
                        'containers': [{
                            'name': field_values['container_name'],
                            'image': field_values['container_image'],
                            'ports': yaml.safe_load(field_values['container_ports']),
                            'env': yaml.safe_load(field_values['environment_variables']),
                            'volumeMounts': yaml.safe_load(field_values['volume_mounts'])
                        }],
                        'volumes': yaml.safe_load(field_values['volumes']),
                        'imagePullSecrets': yaml.safe_load(field_values['image_pull_secrets'])
                    }
                }
            }
        }
    elif resource_type == 'Service':
        return {
            'apiVersion': 'v1',
            'kind': 'Service',
            'metadata': {
                'name': field_values['name'],
                'namespace': field_values['namespace']
            },
            'spec': {
                'type': field_values['type'],
                'ports': yaml.safe_load(field_values['ports']),
                'selector': yaml.safe_load(field_values['selector'])
            }
        }
    elif resource_type == 'Namespace':
        return {
            'apiVersion': 'v1',
            'kind': 'Namespace',
            'metadata': {
                'name': field_values['name'],
                'labels': yaml.safe_load(field_values['labels'])
            }
        }
    elif resource_type == 'Secret':
        return {
            'apiVersion': 'v1',
            'kind': 'Secret',
            'metadata': {
                'name': field_values['name'],
                'namespace': field_values['namespace']
            },
            'type': field_values['type'],
            'data': yaml.safe_load(field_values['data']),
            'stringData': yaml.safe_load(field_values['string_data'])
        }
    elif resource_type == 'ConfigMap':
        return {
            'apiVersion': 'v1',
            'kind': 'ConfigMap',
            'metadata': {
                'name': field_values['name'],
                'namespace': field_values['namespace']
            },
            'data': yaml.safe_load(field_values['data']),
            'binaryData': yaml.safe_load(field_values['binary_data'])
        }
    return {}
