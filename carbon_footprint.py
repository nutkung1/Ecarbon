import streamlit as st
class carbon_footprint:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb
    def carbon_footprint_create(self):
        st.subheader("สร้างข้อมูลคาร์บอนฟุตพริ้นท์")
        cultivated_area_id = st.number_input("ไอดีพื้นที่ปลูก", min_value=1, key="cul_id_footprint")
        total_carbon_footprint = st.number_input("คาร์บอนฟุตพริ้นท์รวม", key="total_carbon_footprint")
        GHG1 = st.number_input("แก๊ส1 (ton/Co2)", key="GHG1")
        GHG2 = st.number_input("แก๊ส2 (ton/Co2)", key="GHG2")
        GHG3 = st.number_input("แก๊ส3 (ton/Co2)", key="GHG3")
        create_button = st.button("สร้าง", key="carbon_footprint_button")
        if create_button:
            self.mycursor.execute("SELECT COUNT(*) FROM carbon_footprint")
            result = self.mycursor.fetchone()[0]
            sql = "insert into carbon_footprint(carbon_footprint_id,cultivated_areas_id, total_carbon_footprint, GHG1, GHG2, GHG3) values(%s,%s,%s,%s,%s,%s)"
            val = (result+1,cultivated_area_id, total_carbon_footprint, GHG1, GHG2, GHG3)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            st.success("สร้างบันทึกสำเร็จ!!!")
    def carbon_footprint_read(self):
        st.subheader("อ่านข้อมูลคาร์บอนฟุตพริ้นท์")
        self.mycursor.execute("SELECT * FROM carbon_footprint")
        result = self.mycursor.fetchall()
        for row in result:
            st.write(row)
    def carbon_footprint_update(self):
        st.subheader("สร้างข้อมูลคาร์บอนฟุตพริ้นท์")
        id = st.number_input("ไอดีคาร์บอนฟุตพริ้นท์", min_value=1, key="carbon_footprint_id")
        cultivated_area_id = st.number_input("ไอดีพื้นที่ปลูก", min_value=1, key="cul_id_footprint_up")
        total_carbon_footprint = st.number_input("คาร์บอนฟุตพริ้นท์รวม", key="total_carbon_footprint_up")
        GHG1 = st.number_input("แก๊ส1 (ton/Co2)", key="GHG1_up")
        GHG2 = st.number_input("แก๊ส2 (ton/Co2)", key="GHG2_up")
        GHG3 = st.number_input("แก๊ส3 (ton/Co2)", key="GHG3_up")
        update_button = st.button("อัพเดท", key="carbon_footprint_button")
        if update_button:
            sql = "UPDATE carbon_footprint set cultivated_areas_id=%s, total_carbon_footprint=%s, GHG1=%s, GHG2=%s, GHG3=%s WHERE carbon_footprint_id=%s"
            val = (cultivated_area_id, total_carbon_footprint, GHG1, GHG2, GHG3, id)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            st.success("อัพเดทข้อมูลสำเร็จ!!!")
    def carbon_footprint_delete(self):
        st.subheader("ลบข้อมูลคาร์บอนฟุตพริ้นท์")
        id = st.number_input("ไอดีคาร์บอนฟุตพริ้นท์", min_value=1, key="carbon_footprint_del")
        delete_button = st.button("ลบ", key="Delete_button_carbon_footprint")
        if delete_button:
            sql = "DELETE FROM carbon_footprint WHERE carbon_footprint_id=%s"
            val = (id,)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            st.success("ลบข้อมูลสำเร็จ!!!")