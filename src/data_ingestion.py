import os
import sys
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split

from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from utils.common_function import read_yaml

logger = get_logger(__name__)


class DataIngestion:

    def __init__(self, config):
        self.config = config["data_ingestion"]

        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info(
            f"Data ingestion started | "
            f"Bucket: {self.bucket_name} | "
            f"File: {self.file_name}"
        )

    def download_csv_from_gcp(self):
        try:
            # Get project from config
            project_id = self.config.get("project_id")
            if not project_id:
                raise ValueError("project_id not found in config file")

            client = storage.Client(project=project_id)

            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)

            blob.download_to_filename(RAW_FILE_PATH)

            logger.info("CSV file successfully downloaded from GCP")

        except Exception as e:
            logger.error("Error while downloading CSV file")
            raise CustomException(str(e), sys)

    def split_data(self):
        try:
            logger.info("Starting train-test split")

            data = pd.read_csv(RAW_FILE_PATH)

            train_data, test_data = train_test_split(
                data,
                test_size=1 - self.train_test_ratio,
                random_state=42
            )

            train_data.to_csv(TRAIN_FILE_PATH, index=False)
            test_data.to_csv(TEST_FILE_PATH, index=False)

            logger.info(f"Train file saved at {TRAIN_FILE_PATH}")
            logger.info(f"Test file saved at {TEST_FILE_PATH}")

        except Exception as e:
            logger.error("Error while splitting data")
            raise CustomException(str(e), sys)

    def run(self):
        try:
            logger.info("Starting data ingestion pipeline")

            self.download_csv_from_gcp()
            self.split_data()

            logger.info("Data ingestion completed successfully")

        except Exception as ce:
            logger.error(f"Data ingestion failed: {ce}")
            raise ce

        finally:
            logger.info("Data ingestion process finished")


if __name__ == "__main__":

    config = read_yaml(CONFIG_PATH)

    data_ingestion = DataIngestion(config)
    data_ingestion.run()