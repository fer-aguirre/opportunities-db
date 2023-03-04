import pandas as pd

# Import modules
import opportunities_db.data.load as load

# Load data
data_processed = load.data_processed


def update_data(df1, df2):
    # Join dataframes
    df_join = df1.merge(df2, how="outer")
    # Save dataframe as 'csv' file
    df_join.to_csv(data_processed, index=False)
