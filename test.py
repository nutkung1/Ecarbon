# import streamlit as st
# import folium
# from streamlit_folium import folium_static  # Import the required function
#
# def main():
#     # Streamlit app title
#     st.title("Folium Map with Streamlit")
#     with st.form(key='my_form', clear_on_submit=False):
#         lat = st.number_input("ละติจูด", placeholder="ละติจูด", step=1.,format="%.7f")
#         lon = st.number_input("ลองจิจูด", placeholder="ลองจิจูด", step=1.,format="%.7f")
#
#         submit_button = st.form_submit_button(label='ส่ง')
#
#     if lat and lon:
#
#         # Create a Folium map
#         map_div = folium.Map(location=[lat, lon], zoom_start=16)
#         # 14.7644528723
#         # 99.731270398600003
#         geo_json_data = "/Users/suchanatratanarueangrong/Mitrphol_ecarbon/ข้อมูลชาวไร่/ecarbon_MDC.geojson"
#
#         # Add OpenStreetMap tiles
#         tile_layer_div_0 = folium.TileLayer(
#             tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
#             attr="OpenStreetMap contributors",
#             name="OpenStreetMap",
#             overlay=True,
#             control=True,
#         )
#         tile_layer_div_0.add_to(map_div)
#
#         # Define GeoJSON data
#         # geo_json_data = {
#         #     "type": "FeatureCollection",
#         #     "features": [
#         #         {
#         #             "type": "Feature",
#         #             "properties": {},
#         #             "geometry": {
#         #                 "type": "Polygon",
#         #                 "coordinates": [[
#         #                     [-122.399077892527, 37.7934347109497],
#         #                     [-122.398922660838, 37.7934544916178],
#         #                     [-122.398980265018, 37.7937266504805],
#         #                     [-122.399133972495, 37.7937070646238],
#         #                     [-122.399077892527, 37.7934347109497]
#         #                 ]]
#         #             }
#         #         }
#         #     ]
#         # }
#
#         # Add GeoJSON layer to the Folium map
#         geo_json_layer = folium.GeoJson(geo_json_data)
#         geo_json_layer.add_to(map_div)
#
#         # Streamlit component to display the Folium map
#         folium_static(map_div)
#
# if __name__ == "__main__":
#     main()

import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate("./ecarbon-ead53-firebase-adminsdk-b1iav-d2f304bd54.json")
app = firebase_admin.initialize_app(cred, { 'storageBucket' : 'ecarbon-ead53.appspot.com' })
photo_path1 = '/Users/suchanatratanarueangrong/Mitrphol_ecarbon/Streamlit/CRUD_REAL/Picture/ID/1.jpg'
bucket = storage.bucket()
blob = bucket.blob(f'ID/ID{numberofpictureId}.jpg')
blob.upload_from_filename(photo_path1)
photo_path2 = '/Users/suchanatratanarueangrong/Mitrphol_ecarbon/Streamlit/CRUD_REAL/Picture/DEED/1.jpg'
bucket = storage.bucket()
blob = bucket.blob(f'DEED/ID{numberofpicturedeed}.jpg')
blob.upload_from_filename(photo_path2)
print('Photo uploaded successfully!')




