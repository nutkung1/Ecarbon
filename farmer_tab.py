import streamlit as st
import mysql.connector
class FarmerTab:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb
    def create_farmer(self):
        st.subheader("สร้างข้อมูล")
        firstname = st.text_input("ชื่อ", key="firstname_farmer", placeholder="สุชาณัฎ")
        lastname = st.text_input("นามสกุล", key="lastname_farmer", placeholder="รัตนเรืองรอง")
        birthday = st.date_input("วันเกิด", key="birthday_farmer")
        membership = st.date_input("วันที่เริ่มเป็นสมาชิก", key="membership_farmer")
        status = st.text_input("สถานะ", key="status_farmer", placeholder="โสด/ไม่โสด")
        phonenumber = st.text_input("เบอร์โทร", key="phonenumber_farmer", placeholder="0857772222")
        email = st.text_input("อีเมลล์", key="email_farmer", placeholder="mitrphol@gmail.com")
        password = st.text_input("รหัสผ่าน", key="password_farmer", type="password")
        password1 = st.text_input("ยืนยันรหัสผ่าน", key="password_farmer_confirm", type="password")
        create_button = st.button("สร้าง", key="create_button_farmer")
        self.mycursor.execute("SELECT * FROM farmer")
        result = self.mycursor.fetchall()
        if create_button:
            sql = "insert into farmer(farmer_id, farmer_firstname,farmer_lastname,farmer_birthday,farmer_start_membership,farmer_status,phone_number,password,email) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (len(result)+1, firstname, lastname, birthday, membership, status, phonenumber,password,email)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            st.success("Record Created Successfully!!!")
    def read_farmer(self):
        st.subheader("อ่านข้อมูล")
        self.mycursor.execute("SELECT * FROM farmer")
        result = self.mycursor.fetchall()
        for row in result:
            st.write(row)
    def update_farmer(self):
        st.subheader("อัพเดทข้อมูล")
        id = st.number_input("ไอดีชาวไร่", min_value=1)
        firstname = st.text_input("ชื่อ")
        lastname = st.text_input("นามสกุล")
        birthday = st.date_input("วันเกิด")
        membership = st.date_input("วันที่เริ่มเป็นสมาชิก")
        status = st.text_input("สถานะ")
        phonenumber = st.text_input("เบอร์โทร")
        if st.button("อัพเดท"):
            sql = "UPDATE farmer set farmer_firstname=%s, farmer_lastname=%s, farmer_birthday=%s, farmer_start_membership=%s, farmer_status=%s, phone_number=%s WHERE farmer_id=%s"
            val = (firstname, lastname, birthday, membership, status, phonenumber, id)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            st.success("Record Updated Successfully!!!")
    def delete_farmer(self):
        st.subheader("ลบข้อมูล")
        id = st.number_input("ไอดีชาวไร่", min_value=1, key="farmer_id")
        delete_button = st.button("Delete", key="Delete_button_farmer")
        if delete_button:
            sql = "DELETE FROM farmer WHERE farmer_id=%s"
            val = (id,)
            mycursor.execute(sql, val)
            mydb.commit()
            st.success("Record Deleted Successfully!!!")