from sensor.exception import SensorException
import os 
import sys

from sensor.logger import logging
from sensor.utils import dump_csv_file_to_mongodb_collection



if __name__ == '__main__':
    file_path="D:/Sensor Fault 2024/Sensor-Fault-Detection/data/aps_failure_system.csv"
    database_name="sensor"
    collection_name="apsdata"
    dump_csv_file_to_mongodb_collection(file_path, database_name, collection_name)
