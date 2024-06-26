import streamlit as st
import mysql.connector
class Fertilizer_Type_Tab:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb
    def fer_type_create(self):
        st.subheader("สร้างข้อมูลชนิดปุ๋ย")
        fer_type_name = st.text_input("ชนิดปุ๋ย", key="fer_typename")
        fer_des = st.text_input("คำอธิบาย", key="fer_des")
        create_button = st.button("สร้าง", key="create_fertype_button")
        if create_button:
            self.mycursor.execute("SELECT COUNT(*) FROM fertilizer_type")
            result = self.mycursor.fetchone()[0]
            sql = "insert into fertilizer_type(type_name, description) values(%s, %s)"
            val = (fer_type_name,fer_des)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            st.success("สร้างบันทึกสำเร็จ!!!")
    def fer_type_read(self):
        st.subheader("อ่านข้อมูลชนิดปุ๋ย")
        self.mycursor.execute("SELECT * FROM fertilizer_type")
        result = self.mycursor.fetchall()
        for row in result:
            st.write(row)
    def fer_type_update(self):
        st.subheader("อัพเดทข้อมูลชนิดปุ๋ย")
        # up_fer_id = st.number_input("ไอดีชนิดปุ๋ย", key="up_fer_id", min_value=1)
        up_fer_type_name = st.text_input("กรอกชื่อชนิดปุ๋ย", key="up_fer_typename")
        up_fer_des = st.text_input("คำอธิบาย", key="up_fer_des")
        update_button = st.button("อัพเดท", key="update_fertype_button")
        if update_button:
            sql = "UPDATE fertilizer_type set description=%s WHERE type_name=%s"
            val = (up_fer_des, up_fer_type_name)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            st.success("อัพเดทข้อมูลสำเร็จ!!!")
    def fer_type_del(self):
        st.subheader("ลบข้อมูล")
        # id = st.number_input("ไอดีชนิดปุ๋ย", min_value=1, key="fertilizer_del_id")
        fertilizer_type_name = st.selectbox("ชนิดปุ๋ย", ('15-15-15', '10-15-20', '16-16-16', '16-16-8', '16-8-8', '21-7-18', '15-7-18', '20-8-20', '14-6-28', '14-7-35'))
        delete_button = st.button("Delete", key="Delete_button_fertype")
        if delete_button:
            sql = "DELETE FROM fertilizer_type WHERE TYPE_NAME=%s"
            val = (fertilizer_type_name,)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            st.success("ลบข้อมูลสำเร็จ!!!")
