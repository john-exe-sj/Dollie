import logging
import watchtower
import boto3
from .SecretsManager import get_secret

secrets = get_secret()

cw_handler = watchtower.CloudWatchLogHandler(
            log_group=secrets['CLOUD_WATCH_LOG_GROUP'],
            boto3_client=boto3.client("logs", region_name="us-west-2")
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(cw_handler)

