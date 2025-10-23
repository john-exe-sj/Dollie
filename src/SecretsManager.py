# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

import boto3
from botocore.exceptions import ClientError
import os
import json
import logging
import watchtower

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#TODO: Place a secret here 


secrets = None

def get_secret():

    global secrets
    mode = os.getenv("DEPLOYMENT_MODE", "PROD")
    secret_name = "prod/dollie/api_and_config"
    region_name = "us-east-2"

    logger.info(f"Deployment mode - {mode}")
    if mode == "DEV": 
         # Create a Secrets Manager client, using stored credentials.
        session = boto3.session.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv("SECRET_KEY")
        )
    
    elif mode == "PROD":
        # Create a Secrets Manager client via instance role. 
        session = boto3.session.Session()

    client = session.client(
            service_name='secretsmanager',
            region_name=region_name
    )

    if secrets: 
        logger.info(f"Secrets exist - returning secrets")
        return secrets

    else: 

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )

        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            print(e.with_traceback())
            logger.error(f"Error Occurred in Secrets Manager; ClientError - {e.with_traceback()}")
            raise e

        secrets = json.loads(get_secret_value_response['SecretString'])
        cw_handler = watchtower.CloudWatchLogHandler(log_group=secrets['CLOUD_WATCH_LOG_GROUP'])
        # Add the CloudWatch handler to the logger
        logger.addHandler(cw_handler)
        logger.info(f"Secrets retrieved.")
        return secrets