import os
import sys

import pandas as pd
from pandas import DataFrame
import numpy as np
from sklearn.model_selection import train_test_split

from us_visa.data_access.collect_data import CollectData
from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact

from us_visa.exception import USvisaException
from us_visa.logger import logging


class DataIngestion:
    """
    Ingest data from MongoDB
    """
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        """
        :param data_ingestion_config:
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise USvisaException(e, sys)

    def export_data_into_feature_store(self) -> DataFrame:
        """
        Description : Exports data from mongodb to csv file
        Output: Data is returned as an artifact of data ingestion components
        :return:
        """

        try:
            logging.info(f"Export data from mongodb")
            collect_data = CollectData()
            df = collect_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            logging.info(f"The shape of dataframe: {df.shape}")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Saving exported data to feature store file path: {feature_store_file_path}")
            df.to_csv(feature_store_file_path, index=False, header=True)
            return df
        except Exception as e:
            raise USvisaException(e, sys)

    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Split the data into train and test and save them as csv files
        :param dataframe:
        :return:
        """
        try:
            logging.info(f"Splitting the data into train and test")
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Saving training data to: {self.data_ingestion_config.training_file_path}")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            logging.info(f"Saving test data to: {self.data_ingestion_config.test_file_path}")
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)

            logging.info(f"Saved training and test data")
        except Exception as e:
            raise USvisaException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:

        """
        Description: Runs the export function in the class and split function in the class.
        It results in initiating mongodb connection, export data from mongodb.
        :return:
        """
        try:
            logging.info(f"Initiating data ingestion")
            dataframe = self.export_data_into_feature_store()
            self.split_data_as_train_test(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_file_path,
                                                            test_file_path=self.data_ingestion_config.test_file_path)
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            logging.info(f"Data ingestion artifact saved")
            return data_ingestion_artifact
        except Exception as e:
            raise USvisaException(e, sys)