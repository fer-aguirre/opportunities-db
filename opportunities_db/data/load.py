# Import module
import opportunities_db.utils.paths as paths

# Inputs
data_raw = paths.data_raw_dir("opportunities_urls.csv")
new_version = paths.assets_dir('new_version.csv')

# Outputs
data_processed = paths.data_processed_dir("opportunities_db.csv")
sqlite = paths.data_processed_dir("opportunities.db")