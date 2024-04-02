import streamlit as st
import mysql.connector
class Fertilizer_Type_Tab:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb
    def fer_type_create(self):
        st.subheader("สร้างข้อมูลชนิดปุ๋ย")
        fer_type_name = st.text_input("กรอกชื่อชนิดปุ๋ย", key="fer_typename")
        fer_des = st.text_input("คำอธิบาย", key="fer_des")
        create_button = st.button("สร้าง", key="create_fertype_button")
        self.mycursor.execute("SELECT * FROM fertilizer_type")
        result = self.mycursor.fetchall()
        if create_button:
            sql = "insert into fertilizer_type(FERTILIZER_TYPE_ID,type_name, description) values(:1,:2,:3)"
            val = (len(result)+1,fer_type_name,fer_des)
            self.mycursor.execute(sql, val)
            self.mydb._instance.commit()
            st.success("สร้างบันทึกสำเร็จ!!!")
    def fer_type_read(self):
        st.subheader("อ่านข้อมูลชนิดปุ๋ย")
        self.mycursor.execute("SELECT * FROM fertilizer_type")
        result = self.mycursor.fetchall()
        for row in result:
            st.write(row)
    def fer_type_update(self):
        st.subheader("อัพเดทข้อมูลชนิดปุ๋ย")
        up_fer_id = st.number_input("ไอดีชนิดปุ๋ย", key="up_fer_id", min_value=1)
        up_fer_type_name = st.text_input("กรอกชื่อชนิดปุ๋ย", key="up_fer_typename")
        up_fer_des = st.text_input("คำอธิบาย", key="up_fer_des")
        update_button = st.button("อัพเดท", key="update_fertype_button")
        if update_button:
            sql = "UPDATE fertilizer_type set type_name=?, description=? WHERE fertilizer_type_id=?"
            val = (up_fer_type_name, up_fer_des, up_fer_id)
            self.mycursor.execute(sql, val)
            self.mydb._instance.commit()
            st.success("อัพเดทข้อมูลสำเร็จ!!!")
    def fer_type_del(self):
        st.subheader("ลบข้อมูล")
        id = st.number_input("ไอดีชนิดปุ๋ย", min_value=1, key="fertilizer_del_id")
        delete_button = st.button("Delete", key="Delete_button_fertype")
        if delete_button:
            sql = "DELETE FROM fertilizer_type WHERE fertilizer_type_id=?"
            val = (id,)
            self.mycursor.execute(sql, val)
            self.mydb._instance.commit()
            st.success("Record Deleted Successfully!!!")
