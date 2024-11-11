import boto3

import base64

from azure.storage.blob import BlockBlobService, ContainerPermissions

from datetime import datetime, timedelta

from botocore.exceptions import ClientError

import json

import os

 

def myconverter(o):

    if isinstance(o, datetime):

        return o.__str__()

 

def lambda_handler(event, context):

    secret_name = "Blobfish"

    region_name = "us-east-1"

    if os.environ.get('ENVIRONMENT', "") == "prod":

        bucket_name = "naapi-ingestion-data"

    else:

        bucket_name = "naapi-ingestion-data-dev"

 

    # Create a Secrets Manager client

    secrets_manager = boto3.client(

        service_name= 'secretsmanager',

        region_name= region_name

    )

 

    s3 = boto3.client(

        service_name= 's3',

        region_name= region_name

    )

 

    get_secret_value_response = secrets_manager.get_secret_value(

        SecretId = secret_name

    )

 

    # Decrypts secret using the associated KMS CMK.

    # Depending on whether the secret is a string or binary, one of these fields will be populated.

    # print(json.dumps(get_secret_value_response, default=myconverter))

    if 'SecretString' in get_secret_value_response:

        key = json.loads(get_secret_value_response['SecretString'])['account_key']

    else:

        decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])

 

    blob_service = BlockBlobService(account_name = 'resourcegraphstorage', account_key = key)

    container = 'resourcegraphcontainer'

    blob_name = 'SavedFileJSON.json'

 

    blob_service.get_blob_to_path(container, blob_name, '/tmp/' + 'azureResourceGraphDataRaw.json')

 

    with open("/tmp/azureResourceGraphDataRaw.json", 'r') as jsonFile:

        data = json.load(jsonFile)

  

    def recursion(obj):

        if type(obj) is str or type(obj) is int:

            return(obj)

        if type(obj) is list:

            for i, item in enumerate(obj):

                obj[i] = recursion(item)

        if type(obj) is dict:

            for key in obj:

                if type(obj[key]) is dict or type(obj[key]) is list:

                    obj[key] = recursion(obj[key])

                elif obj[key] == "":

                    obj[key] = None

        return(obj)

 

    d = recursion(data)

 

    with open('/tmp/' + 'azureResourceGraphData.json', 'w') as file:

        json.dump(d, file, sort_keys=True, indent=2)

 

    s3.upload_file('/tmp/' + 'azureResourceGraphData.json', bucket_name, 'azure/graph/' + 'azureResourceGraphData.json')
