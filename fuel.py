import streamlit as st
class Fuel_Tab:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb
    def fuel_create(self):
        st.subheader("สร้างข้อมูลน้ำมัน")
        cultivated_area_id = st.number_input("ไอดีพื้นที่ปลูก", min_value=1, key="cul_id")
        fuel_used = st.number_input("น้ำมันที่ใช้", key="fuel_used")
        create_button = st.button("สร้าง", key="fuel_button")
        self.mycursor.execute("SELECT * FROM fuel")
        result = self.mycursor.fetchall()
        if create_button:
            sql = "insert into fuel(fuel_id, cultivated_areas_id, fuel_used_in_kilogram) values(:1,:2,:3)"
            val = (len(result)+1, cultivated_area_id, fuel_used)
            self.mycursor.execute(sql, val)
            self.mydb._instance.commit()
            st.success("สร้างบันทึกสำเร็จ!!!")
    def fuel_read(self):
        st.subheader("อ่านข้อมูลน้ำมัน")
        self.mycursor.execute("SELECT * FROM fuel")
        result = self.mycursor.fetchall()
        for row in result:
            st.write(row)
    def fuel_update(self):
        st.subheader("อัพเดทข้อมูลน้ำมัน")
        fuel_id = st.number_input("ไอดีน้ำมัน", key="fuel_id", min_value=1)
        cultivated_area_id = st.number_input("ไอดีพื้นที่ปลูก", min_value=1, key="cul_id")
        fuel_used = st.number_input("น้ำมันที่ใช้", key="fuel_used")
        update_button = st.button("อัพเดท", key="fuel_update")
        if update_button:
            sql = "UPDATE fuel set cultivated_areas_id=?, fuel_used_in_kilogram=? WHERE fuel_id=?"
            val = (cultivated_area_id, fuel_used, fuel_id)
            self.mycursor.execute(sql, val)
            self.mydb._instance.commit()
            st.success("อัพเดทข้อมูลสำเร็จ!!!")
    def fuel_delete(self):
        st.subheader("ลบข้อมูล")
        id = st.number_input("ไอดีน้ำมัน", min_value=1, key="fuel_id_1")
        delete_button = st.button("ลบ", key="Delete_button_fuel")
        if delete_button:
            sql = "DELETE FROM fuel WHERE fuel_id=?"
            val = (id,)
            self.mycursor.execute(sql, val)
            self.mydb._instance.commit()
            st.success("Record Deleted Successfully!!!")