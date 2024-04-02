import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
import mysql.connector
import os
import snowflake.connector

# Establish database connection
mydb = st.connection("snowflake")
account = "PVFGFAY-IY52619"
#account = "gp94921.ap-southeast-1"
user = "suchanat"
password = "NuT0863771558-"
role = "ACCOUNTADMIN"
warehouse = "COMPUTE_WH"
database = "ECARBON"
schema = "ECARBON"

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
        birthday = st.date_input(":blue[วันเกิด]", key="birthday_farmer")
        membership = st.date_input(":blue[วันที่เริ่มเป็นสมาชิก]", key="membership_farmer")
        status = st.text_input(":blue[สถานะ]", key="status_farmer", placeholder="โสด/ไม่โสด")
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
                                    st.session_state['Myimage'] = picture
                                if st.session_state['Myimage']:
                                    fileName = st.session_state['Myimage'].name
                                    new_path = "/Users/suchanatratanarueangrong/Mitrphol_ecarbon/Streamlit/CRUD_REAL/Picture/ID"
                                    file_count = 0
                                    for item in os.listdir(new_path):
                                        if os.path.isfile(os.path.join(new_path, item)):
                                            file_count += 1
                                    fileName = os.path.join(new_path, f"{file_count+1}.jpg")
                                    with open(fileName, "wb") as file:
                                        file.write(st.session_state['Myimage'].getbuffer())
                                        st.success("บันทึกรูปภาพสำเร็จ")
                                    hashed_password = stauth.Hasher([password1]).generate()
                                    sql = "insert into farmer(farmer_id, farmer_firstname,farmer_lastname,farmer_birthday,farmer_start_membership,farmer_status,phone_number,password,email,image) values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)"
                                    val = (file_count+1, firstname,lastname, birthday, membership, status, phonenumber, hashed_password[0], email, fileName)
                                    mycursor.execute(sql, val)
                                    mydb._instance.commit()
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
#     main()
