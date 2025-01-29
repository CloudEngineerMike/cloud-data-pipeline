import os
import json
import base64
import boto3
from datetime import datetime
from azure.storage.blob import BlockBlobService
from botocore.exceptions import ClientError


def myconverter(o):
    """Converts datetime objects to string format."""
    if isinstance(o, datetime):
        return o.__str__()


def lambda_handler(event, context):
    """AWS Lambda handler function."""
    secret_name = "SECRET-NAME"
    region_name = "REGION"

    bucket_name = (
        "S3-BUCKET"
        if os.environ.get("ENVIRONMENT", "") == "prod"
        else "S3-BUCKET-dev"
    )

    # Create AWS Secrets Manager client
    secrets_manager = boto3.client("secretsmanager", region_name=region_name)

    # Create AWS S3 client
    s3 = boto3.client("s3", region_name=region_name)

    # Retrieve secret from AWS Secrets Manager
    get_secret_value_response = secrets_manager.get_secret_value(SecretId=secret_name)

    # Extract secret key
    if "SecretString" in get_secret_value_response:
        key = json.loads(get_secret_value_response["SecretString"])["account_key"]
    else:
        decoded_binary_secret = base64.b64decode(get_secret_value_response["SecretBinary"])
        key = decoded_binary_secret.decode("utf-8")

    # Initialize Azure Blob Storage client
    blob_service = BlockBlobService(account_name="STORAGE-ACCOUNT", account_key=key)
    container = "STORAGE-CONTAINER"
    blob_name = "DATA.json"
    local_blob_path = "/tmp/QUERY-DATA.json"

    # Download blob from Azure
    blob_service.get_blob_to_path(container, blob_name, local_blob_path)

    # Load JSON file
    with open(local_blob_path, "r") as json_file:
        data = json.load(json_file)

    def recursion(obj):
        """Recursively processes JSON data, replacing empty strings with None."""
        if isinstance(obj, (str, int)):
            return obj
        if isinstance(obj, list):
            return [recursion(item) for item in obj]
        if isinstance(obj, dict):
            return {key: recursion(value) if isinstance(value, (dict, list)) else (None if value == "" else value) for key, value in obj.items()}
        return obj

    # Process the JSON data
    processed_data = recursion(data)

    # Save processed JSON data
    processed_json_path = "/tmp/RESOURCE-GRAPH-DATA.json"
    with open(processed_json_path, "w") as file:
        json.dump(processed_data, file, sort_keys=True, indent=2)

    # Upload processed JSON to S3
    s3.upload_file(processed_json_path, bucket_name, "azure/graph/RESOURCE-GRAPH-DATA.json")
