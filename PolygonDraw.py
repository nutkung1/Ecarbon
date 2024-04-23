import streamlit as st
import folium
from streamlit_folium import folium_static
import firebase_admin
from firebase_admin import credentials, storage
import requests
import datetime
import os
from dotenv import load_dotenv

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
def fetch_geojson_from_firebase(file_path):
    bucket = storage.bucket()
    blob = bucket.blob(file_path)

    # Get a temporary download URL for the GeoJSON file
    download_url = blob.generate_signed_url(expiration=datetime.timedelta(minutes=5))

    # Fetch the GeoJSON data using the URL
    response = requests.get(download_url)
    response.raise_for_status()

    return response.json()


def polygon():
    # Streamlit app title
    st.title("ตรวจเช็คขอบเขตพื้นที่")
    with st.form(key='my_form', clear_on_submit=False):
        search = st.text_input("ชื่อชาวไร่", placeholder="ชื่อชาวไร่")
        submit_button = st.form_submit_button(label='ส่ง')

    # Fetch GeoJSON data from Firebase Storage
    geo_json_data = fetch_geojson_from_firebase("ecarbon_MDC.geojson")

    # Initialize the Folium map
    map_div = folium.Map(location=[13.736717, 100.523186], zoom_start=15)

    if search:
        found = False
        for feature in geo_json_data['features']:
            farmer_name = feature['properties'].get('ชื่อชาวไร่')
            if farmer_name and search in farmer_name:
                # Extract the coordinates
                coordinates = feature['geometry']['coordinates'][0][0]
                lat, lon = coordinates[1], coordinates[0]

                # Print the result
                st.write("พบข้อมูลสำหรับชื่อชาวไร่:", farmer_name)
                st.write("Latitude:", lat)
                st.write("Longitude:", lon)

                # Add marker to the map
                folium.Marker(location=[lat, lon], popup=farmer_name).add_to(map_div)

                # Update map view to focus on the coordinates of the searched farmer
                map_div.location = [lat, lon]
                map_div.zoom_start = 15  # Adjust zoom level as needed

                found = True

        if not found:
            st.write("ไม่พบข้อมูลสำหรับชื่อชาวไร่:", search)

    # Add GeoJSON layer to the Folium map
    folium.GeoJson(geo_json_data).add_to(map_div)

    # Streamlit component to display the Folium map
    folium_static(map_div)

