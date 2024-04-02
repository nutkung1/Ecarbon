import streamlit as st
import mysql.connector
import os
class CultivatedTab:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb
    def create_farmer(self):
        st.subheader("สร้างข้อมูล")
        farmer_id = st.number_input("ไอดีชาวไร่", min_value=1, key="farmer_id")
        cultivated_area = st.number_input("พื้นที่ปลูก (ไร่)", key="cultivated_area")
        latitude = st.text_input("ละจิจูด", key="latitude")
        longitude = st.text_input("ลองจิจูด", key="longitude")
        deed = st.file_uploader("อัพโหลดไฟล์โฉนดที่ดิน", type=["jpg", "png"])
        create_button = st.button("สร้าง", key="create button")
        if create_button:
            self.mycursor.execute("SELECT COUNT(*) FROM cultivated_areas")
            result = self.mycursor.fetchone()[0]
            new_path = "/Users/suchanatratanarueangrong/Mitrphol_ecarbon/Streamlit/CRUD_REAL/Picture/DEED"
            fileName = os.path.join(new_path, f"{result + 1}.jpg")
            with open(fileName, "wb") as file:
                file.write(deed.getbuffer())
                st.success("สร้างบันทึกสำเร็จ!!!")
            sql = "INSERT INTO cultivated_areas (Cultivated_areas_id, farmer_id, cultivated_areas_in_rai, latitude, longitude, deed) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (result + 1, farmer_id, cultivated_area, latitude, longitude, fileName)

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
            sql = "UPDATE cultivated_areas SET farmer_id = ?, cultivated_areas_in_rai = ?, latitude = ?, longitude = ? WHERE cultivated_areas_id = ?"
            val = (farmer_id, cultivated_area, latitude, longitude, id)
            self.mycursor.execute(sql, val)
            self.mydb._instance.commit()
            st.success("อัพเดทข้อมูลสำเร็จ!!!")

    def delete_farmer(self):
        st.subheader("ลบข้อมูล")
        id = st.number_input("ไอดีพื้นที่ปลูก", min_value=1, key="del_cultivated_id")
        delete_button = st.button("Delete", key="delete_button_cul")
        if delete_button:
            sql = "DELETE FROM cultivated_areas WHERE cultivated_areas_id = ?"
            val = (id,)
            self.mycursor.execute(sql, val)
            self.mydb._instance.commit()
            st.success("Record Deleted Successfully!!!")
