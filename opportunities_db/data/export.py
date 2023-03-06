import pandas as pd

# Import modules
import opportunities_db.data.load as load

# Load data
data_processed = load.data_processed
last_version = load.last_version


def update_data(df):
    """
    Function to save dataframe as csv file

    df: pandas.DataFrame
    """
    # Save dataframe as 'csv' file
    df.to_csv(data_processed, index=False)


def update_last_version(df1, df2):
    """
    Function to merge two dataframes and save as csv file

    df1: pandas.DataFrame
    df2: pandas.DataFrame
    """
    # Join dataframes
    df_join = df1.merge(df2, how="outer")
    # Save dataframe as 'csv' file
    df_join.to_csv(last_version, index=False)
