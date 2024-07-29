from kubernetes import client
from datetime import datetime

class Workloads:
    def __init__(self):
        self.v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()

    def list_pods_detailed(self):
        pods = self.v1.list_pod_for_all_namespaces(watch=False)
        pod_details = []
        for pod in pods.items:
            status = pod.status.phase
            restarts = sum([container.restart_count for container in pod.status.container_statuses])
            age = self.calculate_age(pod.metadata.creation_timestamp)
            pod_details.append({
                'name': pod.metadata.name,
                'namespace': pod.metadata.namespace,
                'status': status,
                'restarts': restarts,
                'age': age
            })
        return pod_details

    def list_deployments_detailed(self):
        deployments = self.apps_v1.list_deployment_for_all_namespaces()
        deployment_details = []
        for dep in deployments.items:
            conditions = ', '.join([cond.type for cond in dep.status.conditions if cond.status == "True"])
            age = self.calculate_age(dep.metadata.creation_timestamp)
            deployment_details.append({
                'name': dep.metadata.name,
                'namespace': dep.metadata.namespace,
                'pods': f"{dep.status.ready_replicas}/{dep.status.replicas}",
                'replicas': dep.status.replicas,
                'age': age,
                'conditions': conditions
            })
        return deployment_details

    def calculate_age(self, start_time):
        delta = datetime.now(start_time.tzinfo) - start_time
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if days > 0:
            return f"{days}d"
        elif hours > 0:
            return f"{hours}h"
        elif minutes > 0:
            return f"{minutes}m"
        else:
            return f"{seconds}s"
