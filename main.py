import boto3
import json
import datetime
import sys

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)

# Connect to the AWS STS service
sts_client = boto3.client('sts')

# Get the AWS account associated with the credentials
aws_account = sts_client.get_caller_identity()['Account']

# Connect to the ECS service
ecs_client = boto3.client('ecs')

# Get a list of all ECS clusters in the AWS account
cluster_list = ecs_client.list_clusters()['clusterArns']

container_data_list = []

# Loop through each ECS cluster
for cluster in cluster_list:
    # Get a list of all ECS containers in the cluster
    container_list = ecs_client.list_container_instances(cluster=cluster)['containerInstanceArns']

    # Loop through each ECS container
    for container in container_list:
        # Get the JSON data for the container
        container_data = ecs_client.describe_container_instances(cluster=cluster, containerInstances=[container])['containerInstances'][0]
        container_data_list.append(container_data)
        print(f"Added data for container: {container}")

filename = "container_data.json"
with open(filename, "w") as outfile:
    json.dump(container_data_list, outfile, indent=4, cls=JSONEncoder)

print(f"Saved data for {len(container_data_list)} containers to file: {filename}")
