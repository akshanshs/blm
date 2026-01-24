import sys
from us_visa.logger import logging
from us_visa.exception import USvisaException

from us_visa.components.data_ingestion import DataIngestion
from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact


class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        logging.info(f"Data ingestion config created")

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        This method of TrainPipeline class is responsible for data ingestion
        :return:
        """
        try:
            logging.info(f"Starting data ingestion from mongodb")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e

    def run_pipeline(self) -> None:
        """
        This method of TrainPipeline class is responsible for running complete pipeline
        :return:
        """
        try:
            data_ingestion_artifact = self.start_data_ingestion()

        except Exception as e:
            raise USvisaException(e, sys) from e