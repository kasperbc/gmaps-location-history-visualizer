from yaml import load, Loader
import logging
import json
import pandas as pd
import plotly.express as px

logging.basicConfig(format='%(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)

with open('config.yaml', 'r') as f:
    config = load(f, Loader=Loader)


logging.info("Reading config...")
file_name = config['file_name']
if not ".json" in file_name:
    logging.error("The records file must be a json file. Please check that you have added the file extension to the file name in the config.yaml file.")
    exit()

# Read the records
logging.info("Reading records... This may take a moment.")
try:
    file = open(file=file_name, mode='r').read()
except FileNotFoundError:
    logging.error(f"The file {file_name} does not exist. Please check the file name in the config.yaml file.")
    exit()

# Parse the records
logging.info("Parsing json... This may take a moment.")
try:
    records = json.loads(file)
except json.JSONDecodeError:
    logging.error("The file is not a valid json file.")
    exit()

logging.info("Generating map...")
# Extract the latitude and longitude from the records
lat_lon_records = []

for location_record in records["locations"]:
    lat = location_record["latitudeE7"] / 10**7
    lon = location_record["longitudeE7"] / 10**7
    
    lat_lon_records.append((lat, lon))

# Create a dataframe from the records
df = pd.DataFrame(lat_lon_records, columns=["Latitude", "Longitude"])

# Create a map
fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", zoom=10)
if config['heatmap'] == True:
    fig = px.density_mapbox(df, lat="Latitude", lon="Longitude", radius=2, zoom=10)
fig.update_layout(mapbox_style="open-street-map")
fig.show()