# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/


import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_secret():
    load_dotenv()
    mode = os.getenv("DEPLOYMENT_MODE", "DEV").upper()

    logger.info(f"Deployment mode - {mode}")

    if mode == "DEV":
        secrets = {
            "DOLLIES_ANTHROPIC_KEY": os.getenv("DOLLIES_ANTHROPIC_KEY"),
            "MODEL_NAME": os.getenv("MODEL_NAME"),
            "APP_COMMAND_PREFIX": os.getenv("APP_COMMAND_PREFIX"),
            "LIST_OF_ACCEPTABLE_CHANNELS": os.getenv("LIST_OF_ACCEPTABLE_CHANNELS"),
            "DISCORD_BOT_TOKEN": os.getenv("DISCORD_BOT_TOKEN"),
        }

    elif mode == "PROD":
        raise NotImplementedError("AWS Secrets Manager integration is not configured.")
    else:
        raise ValueError(f"Unsupported deployment mode: {mode}")

    """
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
        """
        # CloudWatch logging is disabled.
        # cw_handler = watchtower.CloudWatchLogHandler(
        #     log_group=secrets['CLOUD_WATCH_LOG_GROUP'],
        #     boto3_client=boto3.client("logs", region_name=os.getenv('AWS_DEFAULT_REGION'))
        # )
        # logger.addHandler(cw_handler)

    missing = [name for name, value in secrets.items() if not value]
    if missing:
        raise RuntimeError(f"Missing required configuration: {', '.join(missing)}")

    logger.info("Secrets retrieved.")
    return secrets