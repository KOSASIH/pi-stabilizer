from google.oauth2 import service_account
from googleapiclient.discovery import build

class GCPCloud:
    def __init__(self, credentials_file, project_id, zone):
        self.credentials = service_account.Credentials.from_service_account_file(credentials_file)
        self.compute = build('compute', 'v1', credentials=self.credentials)
        self.storage = build('storage', 'v1', credentials=self.credentials)

    def create_instance(self, instance_name, machine_type, image_project, image_family):
        # Create a new GCP instance
        body = {
            'name': instance_name,
            'machineType': f'zones/{zone}/machineTypes/{machine_type}',
            'disks': [{
                'initializeParams': {
                    'diskSizeGb': '10'
                }
            }],
            'networkInterfaces': [{
                'network': f'global/networks/default'
            }],
            'bootDisk': {
                'initializeParams': {
                    'diskSizeGb': '10'
                }
            }
        }
        response = self.compute.instances().insert(project=project_id, zone=zone, body=body).execute()
        instance_id = response['targetLink']
        return instance_id

    def create_bucket(self, bucket_name):
        # Create a new GCP bucket
        body = {
            'name': bucket_name
        }
        response = self.storage.buckets().insert(project=project_id, body=body).execute()
        bucket_name = response['name']
        return bucket_name

    def upload_file(self, bucket_name, file_name, file_content):
        # Upload a file to GCP bucket
        body = {
            'name': file_name
        }
        response = self.storage.objects().insert(bucket=bucket_name, body=body, media_body=file_content).execute()
        return response
