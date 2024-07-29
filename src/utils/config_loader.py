from kubernetes import config

def load_config(config_path):
    try:
        config.load_kube_config(config_file=config_path)
        return True
    except Exception as e:
        raise Exception(f"Failed to load kubeconfig: {str(e)}")
