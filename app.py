import os

from dotenv import load_dotenv
from us_visa.constants import MONGODB_URL_KEY
from us_visa.components.data_ingestion import DataIngestion
from us_visa.entity.config_entity import DataIngestionConfig

load_dotenv()

print(os.getenv(MONGODB_URL_KEY))
config = DataIngestionConfig()
data = DataIngestion(config)

artifact = data.initiate_data_ingestion()