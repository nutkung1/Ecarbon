import streamlit as st
import mysql.connector
import os
import firebase_admin
from firebase_admin import credentials, storage
from dotenv import load_dotenv


class CultivatedTab:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb

    def configure(self):
        load_dotenv()

    def configure_firebase(self):
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
                'type': firebase_type,
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

            app = firebase_admin.initialize_app(cred, {'storageBucket': 'ecarbon-ead53.appspot.com'})

    def upload_image_to_firebase(self, image_data, result):
        """Uploads an image to Firebase Storage.

        Args:
            image_data (bytes): The image data in bytes format.
            result (int): Count of cultivated areas.

        Returns:
            str: The upload URL for the image in Firebase Storage, or None if an error occurs.
        """

        bucket = storage.bucket()
        try:
            # Generate a unique filename to avoid conflicts
            filename = f'DEED/{result + 1}'  # Example filename pattern
            blob = bucket.blob(filename)
            blob.upload_from_string(image_data, content_type='image/jpeg')  # Adjust content type if needed
            return blob.public_url  # Make the image publicly accessible (optional)
        except Exception as e:
            print(f"Error uploading image: {e}")
            return None

    def create_farmer(self):
        st.subheader("สร้างข้อมูล")
        farmer_id = st.number_input("ไอดีชาวไร่", min_value=1, key="farmer_id")
        cultivated_area = st.number_input("พื้นที่ปลูก (ไร่)", key="cultivated_area")
        latitude = st.text_input("ละจิจูด", key="latitude")
        longitude = st.text_input("ลองจิจูด", key="longitude")
        deed = st.file_uploader("อัพโหลดไฟล์โฉนดที่ดิน", type=["jpg", "png"])
        create_button = st.button("สร้าง", key="create_button")
        if create_button:
            self.mycursor.execute("SELECT COUNT(*) FROM cultivated_areas")
            result = self.mycursor.fetchone()[0]
            upload_url = self.upload_image_to_firebase(deed.read(), result)
            sql = "INSERT INTO cultivated_areas (Cultivated_areas_id, farmer_id, cultivated_areas_in_rai, latitude, longitude, deed) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (result + 1, farmer_id, cultivated_area, latitude, longitude, upload_url)

            self.mycursor.execute(sql, val)
            self.mydb.commit()
            st.success("สร้างบันทึกสำเร็จ!!!")

    def read_farmer(self):
        st.subheader("อ่านข้อมูล")
        self.mycursor.execute("SELECT * FROM cultivated_areas")
        result = self.mycursor.fetchall()
        for row in result:
            st.write(row)

    def update_farmer(self):
        st.subheader("อัพเดทข้อมูล")
        id = st.number_input("ไอดีพื้นที่ปลูก", min_value=1, key="cultivated_id")
        farmer_id = st.number_input("ไอดีชาวไร่", min_value=1, key="farmer_id")
        cultivated_area = st.number_input("พื้นที่ปลูก (ไร่)", key="cultivated_area")
        latitude = st.text_input("ละจิจูด", key="latitude")
        longitude = st.text_input("ลองจิจูด", key="longitude")
        update_button = st.button("อัพเดท", key="update_button")
        if update_button:
            sql = "UPDATE cultivated_areas SET farmer_id = %s, cultivated_areas_in_rai = %s, latitude = %s, longitude = %s WHERE cultivated_areas_id = %s"
            val = (farmer_id, cultivated_area, latitude, longitude, id)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            st.success("อัพเดทข้อมูลสำเร็จ!!!")

    def delete_farmer(self):
        st.subheader("ลบข้อมูล")
        id = st.number_input("ไอดีพื้นที่ปลูก", min_value=1, key="del_cultivated_id")
        delete_button = st.button("Delete", key="delete_button_cul")
        if delete_button:
            sql = "DELETE FROM cultivated_areas WHERE cultivated_areas_id = %s"
            val = (id,)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            st.success("Record Deleted Successfully!!!")
