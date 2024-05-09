import streamlit as st
import streamlit_authenticator as stauth
import re
import mysql.connector
import os
import snowflake.connector
import firebase_admin
from firebase_admin import credentials, storage
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

# Establish database connection
account = os.getenv('account')
user = os.getenv('user_snow')
password = os.getenv('password')
role = os.getenv('role')
warehouse = os.getenv('warehouse')
database = os.getenv('database')
schema = os.getenv('schema')
# print(user)
# Create a connection
mydb = snowflake.connector.connect(
    user=user,
    password=password,
    account=account,
    warehouse=warehouse,
    database=database,
    schema=schema
)
mycursor = mydb.cursor()

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

mycursor.execute("SELECT COUNT(*) FROM FARMER")
result = mycursor.fetchone()[0]

def upload_image_to_firebase(image_data):
    """Uploads an image to Firebase Storage.

    Args:
        image_data (bytes): The image data in bytes format.

    Returns:
        str: The upload URL for the image in Firebase Storage, or None if an error occurs.
    """

    bucket = storage.bucket()
    try:
        # Generate a unique filename to avoid conflicts
        filename = f'ID/{result+1}'  # Example filename pattern
        blob = bucket.blob(filename)
        blob.upload_from_string(image_data, content_type='image/jpeg')  # Adjust content type if needed
        return blob.public_url  # Make the image publicly accessible (optional)
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None

def validate_email(email):
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pattern, email):
        return True
    return False

def get_emails():
    mycursor.execute("SELECT email FROM farmer")
    result = mycursor.fetchall()
    email_list = [user[0] for user in result]  # Extracting the email values
    return email_list

def sign_up():
    with st.form(key="signup", clear_on_submit=True):
        if 'Myimage' not in st.session_state.keys():
            st.session_state['Myimage'] = None
        st.subheader(':green[สมัครบัญชี]')
        firstname = st.text_input(":blue[ชื่อ]", key="firstname_farmer", placeholder="สุชาณัฎ")
        lastname = st.text_input(":blue[นามสกุล]", key="lastname_farmer", placeholder="รัตนเรืองรอง")
        birthday = st.date_input(":blue[วันเกิด]", key="birthday_farmer", min_value=datetime.date(year=1920, month=12, day=31))
        membership = st.date_input(":blue[วันที่เริ่มเป็นสมาชิก]", key="membership_farmer")
        # status = st.text_input(":blue[สถานะ]", key="status_farmer", placeholder="โสด/ไม่โสด")
        phonenumber = st.text_input(":blue[เบอร์โทร]", key="phonenumber_farmer", placeholder="0857772222")
        email = st.text_input(":blue[อีเมล]", key="email_farmer", placeholder="mitrphol@gmail.com")
        password = st.text_input(":blue[รหัสผ่าน (ต้องมีมากกว่า 6 ตัว)]", key="password_farmer", type="password")
        password1 = st.text_input(":blue[กรอกรหัสผ่านอีกครั้ง (ต้องตรงกับรหัสผ่านที่กรอกก่อนหน้า)]", key="password_farmer_confirm", type="password")
        picture = st.camera_input("Take a photo", key="camera")

        if email:
            if validate_email(email):
                if email not in get_emails():
                    if len(password) >= 6:
                        if password == password1:
                            if picture:
                                st.session_state['Myimage'] = picture
                                if picture:
                                    st.session_state["image_data"] = picture.getbuffer().tobytes()
                                if st.session_state['Myimage']:
                                    # fileName = st.session_state['Myimage'].name
                                    # new_path = "/Users/suchanatratanarueangrong/Mitrphol_ecarbon/Streamlit/CRUD_REAL/Picture/ID"
                                    upload_url = upload_image_to_firebase(st.session_state["image_data"])
                                    # for item in os.listdir(new_path):
                                    #     if os.path.isfile(os.path.join(new_path, item)):
                                    #         file_count += 1
                                    # fileName = os.path.join(new_path, f"{file_count+1}.jpg")
                                    # with open(fileName, "wb") as file:
                                    #     file.write(st.session_state['Myimage'].getbuffer())
                                    #     st.success("บันทึกรูปภาพสำเร็จ")
                                    # mycursor.execute("SELECT COUNT(*) FROM FARMER")
                                    # result = mycursor.fetchone()[0]
                                    hashed_password = stauth.Hasher([password1]).generate()
                                    print(result+1)
                                    sql = "insert into farmer(farmer_id, farmer_firstname,farmer_lastname,farmer_birthday,farmer_start_membership,phone_number,password,email,image) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                    val = (result+1, firstname,lastname, birthday, membership, phonenumber, hashed_password[0], email, upload_url)
                                    mycursor.execute(sql, val)
                                    mydb.commit()
                                    st.success("ลงทะเบียนเสร็จสมบูรณ์")
                                    st.balloons()
                            else:
                                st.warning("โปรดถ่ายรูป")
                        else:
                            st.warning("รหัสผ่านไม่ตรงกัน")
                    else:
                        st.warning("โปรดใส่รหัสผ่านให้มากกว่า6ตัว")
                else:
                    st.warning("มีอีเมลอยู่ในระบบ")
            else:
                st.warning("อีเมลไม่ถูกต้อง")
        st.form_submit_button("สร้าง")  # Move submit button inside the form

# sign_up()
# def main():
#     sign_up()
#
# if __name__ == "__main__":
#     sign_up()