# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

import boto3
from botocore.exceptions import ClientError
import os
import json

result = None

#TODO: Seperate between dev and prod.

def get_secret():

    global result

    if result: 
        return result

    else: 
        secret_name = "prod/dollie/api_and_config"
        region_name = "us-east-2"

        # Create a Secrets Manager client
        session = boto3.session.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv("SECRET_KEY")
        )

        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            print(e.with_traceback())
            raise e

        result = json.loads(get_secret_value_response['SecretString'])
        return result

