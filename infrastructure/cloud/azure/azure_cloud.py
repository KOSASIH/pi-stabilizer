from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.storage.blob import BlobServiceClient

class AzureCloud:
    def __init__(self, subscription_id, resource_group, location):
        self.credential = DefaultAzureCredential()
        self.compute_client = ComputeManagementClient(self.credential, subscription_id)
        self.blob_service_client = BlobServiceClient(f"https://{resource_group}.blob.core.windows.net", self.credential)

    def create_instance(self, instance_name, vm_size, image_reference):
        # Create a new Azure instance
        body = {
            'location': location,
            'vm_size': vm_size,
            'image_reference': image_reference
        }
        response = self.compute_client.virtual_machines.create_or_update(resource_group, instance_name, body)
        instance_id = response.id
        return instance_id

    def create_container(self, container_name):
        # Create a new Azure blob container
        container_client = self.blob_service_client.create_container(container_name)
        return container_client

    def upload_file(self, container_name, file_name, file_content):
        # Upload a file to Azure blob container
        blob_client = self.blob_service_client.get_blob_client(container_name, file_name)
        response = blob_client.upload_data(file_content, overwrite=True)
        return response
