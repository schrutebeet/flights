import os
from typing import List, Dict


import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime, timedelta


class DataManager:
    
    LAST_HOUR = None

    def __init__(self):
        pass
    
    @staticmethod
    def preprocess_data(list_of_jsons: List[Dict]) -> pd.DataFrame:
        df = pd.DataFrame(list_of_jsons)
        df = df.drop(["type", "geometry_type"], axis=1)
        for prefix in ["geometry", "properties"]:
            df.columns = df.columns.str.replace(f"^{prefix}_", "", regex=True)
        df["landingTimes_estimated"] = pd.to_datetime(pd.to_numeric(df["landingTimes_estimated"]), unit='s')
        df["time_stamp"] = datetime.now()
        return df

    @staticmethod
    def save_to_temp(df, base_temp_folder="./temp_data"):
        """
        Save the DataFrame into a temporary folder organized by day and hour.
        """
        now = datetime.now()
        day_folder = now.strftime("%Y-%m-%d")
        hour_folder = now.strftime("%H")
        
        # Construct folder path
        temp_folder = os.path.join(base_temp_folder, day_folder, hour_folder)
        os.makedirs(temp_folder, exist_ok=True)
        
        # Save DataFrame to a timestamp-based Parquet file
        temp_file = os.path.join(temp_folder, f"data_{now.strftime('%Y%m%d%H%M%S')}.parquet")
        df.to_parquet(temp_file)

        print(f"Saved DataFrame to {temp_file}")

    @staticmethod
    def process_hourly_data(base_temp_folder="./temp_data", output_folder="./output_data", last_hour=None):
        """
        Check if the hour has changed and concatenate all DataFrames from the previous hour
        into a single Parquet file.
        """
        now = datetime.now()
        current_hour = now.hour
        current_day = now.date()
        day_folder = now.strftime("%Y-%m-%d")

        if last_hour is not None and last_hour != current_hour:
            if last_hour == 23 and current_hour == 0:
                # Transition from 23:00 to 00:00
                previous_day = current_day - timedelta(days=1)
                previous_hour = 23
                day_folder = previous_day.strftime("%Y-%m-%d")
            else:
                # Same day
                previous_hour = last_hour
                day_folder = current_day.strftime("%Y-%m-%d")
            # Construct the folder path for the previous hour
            previous_hour_folder = os.path.join(base_temp_folder, day_folder, f"{previous_hour:02d}")

            # Process the data if the folder exists
            if os.path.exists(previous_hour_folder):
                # List all Parquet files in the previous hour folder
                files = [os.path.join(previous_hour_folder, f) for f in os.listdir(previous_hour_folder) if f.endswith(".parquet")]
                
                if files:
                    # Merge all Parquet files into a single file
                    output_file = os.path.join(output_folder, f"{day_folder}_{previous_hour:02d}.parquet")
                    os.makedirs(output_folder, exist_ok=True)
                    DataManager.merge_parquet_files(files, output_file)

                    print(f"Saved merged Parquet file to {output_file}")

                    # Clean up temporary files
                    for f in files:
                        os.remove(f)
                    os.rmdir(previous_hour_folder)

        # Return the current hour as the new "last_hour"
        return current_hour
    
    @staticmethod
    def merge_parquet_files(files, output_file):
        """
        Merge multiple Parquet files directly into one without loading them fully into memory.
        """
        tables = [pq.read_table(f) for f in files]  # Read each file as a PyArrow Table
        combined_table = pa.concat_tables(tables)  # Combine tables
        pq.write_table(combined_table, output_file)  # Write the combined table to a single Parquet file

