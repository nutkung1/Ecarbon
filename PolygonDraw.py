import streamlit as st
import folium
from streamlit_folium import folium_static
import firebase_admin
from firebase_admin import credentials, storage
import requests
import datetime
import os
from dotenv import load_dotenv
import json

def configure():
    load_dotenv()

configure()
if not firebase_admin._apps:
    # Initialize the Firebase app only if it hasn't been initialized before
    firebase_type = os.environ.get('type')
    firebase_project_id = os.environ.get('project_id')
    firebase_private_key_id = os.environ.get('private_key_id')
    firebase_private_key = os.environ.get('private_key')
    firebase_client_email = os.environ.get('client_email')
    firebase_client_id = os.environ.get('client_id')
    firebase_auth_uri = os.environ.get('auth_uri')
    firebase_token_uri = os.environ.get('token_uri')
    firebase_auth_provider = os.environ.get('auth_provider_x509_cert_url')
    firebase_client_x509 = os.environ.get('client_x509_cert_url')
    firebase_universe_domain = os.environ.get('googleapis.com')

    cred = credentials.Certificate({
        'type':firebase_type,
        'project_id': firebase_project_id,
        'private_key_id': firebase_private_key_id,
        'private_key': firebase_private_key.replace(r'\n', '\n'),
        'client_email': firebase_client_email,
        'client_id': firebase_client_id,
        'auth_uri': firebase_auth_uri,
        'token_uri': firebase_token_uri,
        'auth_provider_x509_cert_url': firebase_auth_provider,
        'client_x509_cert_url': firebase_client_x509,
        'universe_domain': firebase_universe_domain
    })

    app = firebase_admin.initialize_app(cred, { 'storageBucket' : 'ecarbon-ead53.appspot.com' })


# Function to fetch GeoJSON data from Firebase Storage
# def fetch_geojson_from_firebase(file_path):
#     bucket = storage.bucket()
#     blob = bucket.blob(file_path)
#
#     # Get a temporary download URL for the GeoJSON file
#     download_url = blob.generate_signed_url(expiration=datetime.timedelta(minutes=5))
#
#     # Fetch the GeoJSON data using the URL
#     response = requests.get(download_url)
#     response.raise_for_status()
#
#     return response.json()
def fetch_geojson_from_firebase(file_path):
    bucket = storage.bucket()
    blob = bucket.blob(file_path)

    # Download the GeoJSON file to a temporary file
    temp_file = "/tmp/temp_geojson.json"  # Temporary file path
    blob.download_to_filename(temp_file)

    # Read the downloaded GeoJSON file
    with open(temp_file, "r") as f:
        geojson_data = json.load(f)

    return geojson_data

def polygon():
    # Streamlit app title
    st.title("ตรวจเช็คขอบเขตพื้นที่")
    with st.form(key='my_form', clear_on_submit=False):
        lat = st.number_input("ละติจูด", placeholder="ละติจูด", step=1.,format="%.7f")
        lon = st.number_input("ลองจิจูด", placeholder="ลองจิจูด", step=1.,format="%.7f")

        submit_button = st.form_submit_button(label='ส่ง')

    if lat and lon:

        # Fetch GeoJSON data from Firebase Storage
        geo_json_data = fetch_geojson_from_firebase("ecarbon_MDC.geojson")
        map_div = folium.Map(location=[lat, lon], zoom_start=16)

        # Add GeoJSON layer to the Folium map
        geo_json_layer = folium.GeoJson(geo_json_data)
        geo_json_layer.add_to(map_div)

        # Create a Folium map
        # map_div = folium.Map(location=[lat, lon], zoom_start=16)
        # 14.7644528723
        # 99.731270398600003
        # geo_json_data = "/Users/suchanatratanarueangrong/Mitrphol_ecarbon/ข้อมูลชาวไร่/ecarbon_MDC.geojson"

        # Add OpenStreetMap tiles
        tile_layer_div_0 = folium.TileLayer(
            tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr="OpenStreetMap contributors",
            name="OpenStreetMap",
            overlay=True,
            control=True,
        )
        tile_layer_div_0.add_to(map_div)

        # Define GeoJSON data
        # geo_json_data = {
        #     "type": "FeatureCollection",
        #     "features": [
        #         {
        #             "type": "Feature",
        #             "properties": {},
        #             "geometry": {
        #                 "type": "Polygon",
        #                 "coordinates": [[
        #                     [-122.399077892527, 37.7934347109497],
        #                     [-122.398922660838, 37.7934544916178],
        #                     [-122.398980265018, 37.7937266504805],
        #                     [-122.399133972495, 37.7937070646238],
        #                     [-122.399077892527, 37.7934347109497]
        #                 ]]
        #             }
        #         }
        #     ]
        # }

        # Add GeoJSON layer to the Folium map
        geo_json_layer = folium.GeoJson(geo_json_data)
        geo_json_layer.add_to(map_div)

        # Streamlit component to display the Folium map
        folium_static(map_div)

# if __name__ == "__main__":
#     polygon()