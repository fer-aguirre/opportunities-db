# Import module
import opportunities_db.utils.paths as paths

# Inputs
data_raw = paths.data_raw_dir("opportunities_urls.csv")
new_urls = paths.assets_dir("new_urls.csv")
data_processed = paths.data_processed_dir("opportunities_db.csv")
last_version = paths.data_processed_dir("last_version.csv")

# Outputs
data_proc_dir = paths.data_processed_dir()
sqlite = paths.data_processed_dir("opportunities.db")
